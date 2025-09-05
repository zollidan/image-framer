#!/bin/bash

# -------- Проверка переменных окружения --------
if [ -z "$MY_DOMAIN" ]; then
    echo "ОШИБКА: Переменная MY_DOMAIN не задана!"
    echo "Установите её командой: export MY_DOMAIN=your-domain.com"
    exit 1
fi

if [ -z "$OAUTHTOKEN" ]; then
    echo "ОШИБКА: Переменная OAUTHTOKEN не задана!"
    echo "Установите её командой: export OAUTHTOKEN=token"
    exit 1
fi

if [ -z "$REGISTER_ID" ]; then
    echo "ОШИБКА: Переменная REGISTER_ID не задана!"
    echo "Установите её командой: export REGISTER_ID=your-register-id"
    exit 1
fi

echo "$OAUTHTOKEN"|docker login \
  --username oauth \
  --password-stdin \
 cr.yandex

echo "Переменные окружения:"
echo "MY_DOMAIN: $MY_DOMAIN"
echo "REGISTER_ID: $REGISTER_ID"

# -------- Image framer install ---------
# Клонирование репозитория 
if [ -d "image-framer" ]; then
    echo "Директория image-framer уже существует. обновляем её..."
    cd image-framer
    git pull
else
    echo "Клонируем репозиторий image-framer..."    
    git clone https://github.com/zollidan/image-framer.git
    cd image-framer
fi

# Создание .env файла
echo "REGISTER_ID=${REGISTER_ID}" > .env
echo "DOMAIN=${MY_DOMAIN}" >> .env

# Создание шаблона конфигурации nginx внутри проекта
cat > nginx-proxy-template.conf << 'EOF'
server {
    listen 80;
    server_name ${MY_DOMAIN};
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 https://$server_name$request_uri;
    }
}
server {
    listen 443 ssl http2;
    server_name ${MY_DOMAIN};
    ssl_certificate /etc/letsencrypt/live/${MY_DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${MY_DOMAIN}/privkey.pem;
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Проверка наличия docker-compose.yml
if [ ! -f "docker-compose.yml" ] && [ ! -f "compose.yml" ]; then
    echo "ОШИБКА: Файл docker-compose.yml или compose.yml не найден!"
    exit 1
fi

# Создание директорий для SSL сертификатов
mkdir -p ./certbot/conf
mkdir -p ./certbot/www

# Генерация финального nginx конфига
envsubst '${MY_DOMAIN}' < nginx-proxy-template.conf > nginx-proxy.conf

# -------- Получение SSL сертификата (только если его ещё нет) --------
CERT_PATH="./certbot/conf/live/${MY_DOMAIN}/fullchain.pem"

if [ ! -f "$CERT_PATH" ]; then
    echo "Сертификат не найден, запрашиваем новый..."
    
    # Запуск временного nginx на 80 порту
    docker run -d --name temp-nginx \
      -p 80:80 \
      -v $(pwd)/certbot/www:/var/www/certbot \
      nginx:alpine \
      sh -c 'echo "server { listen 80; location /.well-known/acme-challenge/ { root /var/www/certbot; } location / { return 301 https://\$server_name\$request_uri; } }" > /etc/nginx/conf.d/default.conf && nginx -g "daemon off;"'

    # Запрос сертификата
    docker run --rm \
      -v $(pwd)/certbot/conf:/etc/letsencrypt \
      -v $(pwd)/certbot/www:/var/www/certbot \
      certbot/certbot:latest \
      certonly --webroot \
      --webroot-path=/var/www/certbot \
      --email admin@${MY_DOMAIN} \
      --agree-tos \
      --no-eff-email \
      -d ${MY_DOMAIN}

    # Остановка временного nginx
    docker stop temp-nginx && docker rm temp-nginx
else
    echo "Сертификат уже существует, пропускаем выдачу."
fi

# -------- Запуск приложения --------
echo "Запуск Docker Compose..."
docker compose up -d

# Ожидание запуска сервисов
echo "Ожидание запуска сервисов..."
sleep 10

# Проверка статуса контейнеров
echo "Статус контейнеров:"
docker compose ps

echo "✅ Установка завершена!"
echo "Проверьте доступность сервиса по адресу: https://${MY_DOMAIN}"
