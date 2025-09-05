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

echo "$OAUTHTOKEN" | docker login \
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

# Создание директорий для SSL сертификатов
mkdir -p ./certbot/conf
mkdir -p ./certbot/www

# -------- Получение SSL сертификата (только если его ещё нет) --------
CERT_PATH="./certbot/conf/live/${MY_DOMAIN}/fullchain.pem"

if [ ! -f "$CERT_PATH" ]; then
    echo "Сертификат не найден, запрашиваем новый..."
    
    # Запуск временного nginx для Certbot
    docker run --rm \
      -v $(pwd)/certbot/www:/var/www/certbot \
      -v $(pwd)/nginx-proxy.conf:/etc/nginx/nginx.conf:ro \
      nginx:alpine \
      sh -c 'echo "Starting temporary nginx for Certbot..." && nginx -c /etc/nginx/nginx.conf -g "daemon off;"' &
    
    # Ждем, пока временный nginx запустится
    sleep 5

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
      
    # Останавливаем временный nginx
    pkill nginx
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
