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
