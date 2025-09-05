#!/bin/bash

# Обновление системы
sudo apt update
sudo apt upgrade -y
sudo apt install git vim curl ca-certificates -y

# --------Docker install ---------
# Удаление старых версий Docker
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do 
    sudo apt-get remove $pkg -y 2>/dev/null || true
done

# Добавление официального GPG ключа Docker
sudo apt-get update
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Добавление репозитория в источники Apt
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установка Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Проверка установки Docker
sudo systemctl enable docker
sudo systemctl start docker

echo "Docker установлен. Перелогиньтесь для применения изменений группы docker."

# --------SSL Certbot install ---------
# Установка Certbot
sudo apt install snapd -y
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
sudo ln -sf /snap/bin/certbot /usr/bin/certbot

# Альтернативная установка через apt (если snap недоступен)
# sudo apt install certbot python3-certbot-nginx -y

# Проверка переменных окружения
if [ -z "$MY_DOMAIN" ]; then
    echo "ОШИБКА: Переменная MY_DOMAIN не задана!"
    echo "Установите её командой: export MY_DOMAIN=your-domain.com"
    exit 1
fi

if [ -z "$REGISTER_ID" ]; then
    echo "ОШИБКА: Переменная REGISTER_ID не задана!"
    echo "Установите её командой: export REGISTER_ID=your-register-id"
    exit 1
fi

echo "Переменные окружения:"
echo "MY_DOMAIN: $MY_DOMAIN"
echo "REGISTER_ID: $REGISTER_ID"

# --------Image framer install ---------
# Клонирование репозитория
if [ -d "image-framer" ]; then
    echo "Директория image-framer уже существует. Удаляем старую версию..."
    rm -rf image-framer
fi

git clone https://github.com/zollidan/image-framer.git
cd image-framer

# Создание .env файла с правильным форматом
echo "REGISTER_ID=${REGISTER_ID}" > .env
echo "DOMAIN=${MY_DOMAIN}" >> .env

# Проверка наличия docker-compose.yml
if [ ! -f "docker-compose.yml" ] && [ ! -f "compose.yml" ]; then
    echo "ОШИБКА: Файл docker-compose.yml или compose.yml не найден!"
    exit 1
fi

# Запуск контейнеров
echo "Запуск Docker Compose..."
docker compose up -d

# Ожидание запуска сервисов
echo "Ожидание запуска сервисов..."
sleep 10

# Проверка статуса контейнеров
echo "Статус контейнеров:"
docker compose ps

# Создание директорий для SSL сертификатов
mkdir -p ./certbot/conf
mkdir -p ./certbot/www

# Создание конфигураций nginx
envsubst '${MY_DOMAIN}' < nginx-proxy-template.conf > nginx-proxy.conf

# Первоначальный запуск без SSL для получения сертификатов
echo "Запуск временного nginx для получения SSL сертификатов..."
docker run -d --name temp-nginx \
  -p 80:80 \
  -v $(pwd)/certbot/www:/var/www/certbot \
  nginx:alpine \
  sh -c 'echo "server { listen 80; location /.well-known/acme-challenge/ { root /var/www/certbot; } location / { return 301 https://\$server_name\$request_uri; } }" > /etc/nginx/conf.d/default.conf && nginx -g "daemon off;"'

# Получение SSL сертификата
echo "Получение SSL сертификата для домена $MY_DOMAIN..."
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

# Остановка временного контейнера
docker stop temp-nginx && docker rm temp-nginx

echo "Установка завершена!"
echo "Проверьте доступность сервиса по адресу: https://${MY_DOMAIN}"