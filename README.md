# Image Framer

Проект предоставляет простой бэкенд на FastAPI для обработки изображений: добавление рамок и наложение на белый фон. Репозиторий также содержит фронтенд для взаимодействия с API.

## Разработка

### Локальный запуск бэкенда

```bash
cd backend
uv run fastapi run app/main.py --host 0.0.0.0
```

### Тесты

```bash
cd backend
uv run pytest
```

### CI

В репозитории присутствует GitHub Actions workflow, который запускает тесты. Запуск производится вручную через интерфейс GitHub.

---

## Развертывание на продакшене

### Предварительные требования

- Ubuntu 20.04+ сервер с публичным IP
- Доменное имя, направленное на IP сервера
- Yandex Container Registry ID

### 1. Подготовка сервера

Склонируйте репозиторий на сервер:

```bash
git clone https://github.com/zollidan/image-framer.git
cd image-framer
```

### 2. Установка зависимостей

Скрипт установит Docker, Docker Compose и настроит SSL сертификаты:

```bash
chmod +x setup.sh
```

### 3. Настройка переменных окружения

```bash
export MY_DOMAIN="your-domain.com"           # Ваш домен
export REGISTER_ID="your-yandex-registry-id"  # ID в Yandex Container Registry
```

### 4. Запуск установки

```bash
./setup.sh
```

Скрипт выполнит:

- Обновление системы
- Установку Docker и Docker Compose
- Получение SSL сертификатов Let's Encrypt
- Настройку nginx с SSL терминацией
- Запуск всех сервисов

### 5. Проверка развертывания

После успешного запуска проверьте:

```bash
# Статус контейнеров
docker compose ps

# Логи сервисов
docker compose logs frontend
docker compose logs backend
docker compose logs nginx-proxy
```

Приложение будет доступно по адресу: `https://your-domain.com`

## Архитектура развертывания

```
Интернет → nginx-proxy (SSL) → frontend nginx → backend
  HTTPS         HTTP              HTTP            HTTP
```

### Компоненты:

- **nginx-proxy**: SSL терминация (порты 80/443)
- **frontend**: React приложение с nginx (порт 3000)
- **backend**: FastAPI сервер (порт 8000)
- **certbot**: Автообновление SSL сертификатов

## Обслуживание

### Обновление образов

```bash
docker compose pull
docker compose up -d
```

### Просмотр логов

```bash
docker compose logs -f [service_name]
```

### Перезапуск сервисов

```bash
docker compose restart [service_name]
```

### Обновление SSL сертификатов

Сертификаты обновляются автоматически каждые 12 часов через контейнер certbot.

Принудительное обновление:

```bash
docker compose exec certbot certbot renew
docker compose exec nginx-proxy nginx -s reload
```

## Безопасность

- SSL/TLS сертификаты от Let's Encrypt
- Автоматический редирект HTTP → HTTPS
- Безопасные заголовки (HSTS, X-Frame-Options)
- Изолированная Docker сеть

## Мониторинг

### Проверка доступности

```bash
curl -I https://your-domain.com
```

### Статус SSL сертификата

```bash
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

## Устранение неисправностей

### Проблемы с SSL

1. Убедитесь, что домен указывает на IP сервера
2. Проверьте, что порты 80 и 443 открыты
3. Просмотрите логи certbot: `docker compose logs certbot`

### Проблемы с запуском

1. Проверьте переменные окружения в `.env`
2. Убедитесь в наличии образов в registry
3. Просмотрите логи сервисов

### Перезапуск с нуля

```bash
docker compose down -v
docker system prune -f
./setup.sh
```

## Поддержка

Для получения помощи создайте issue в репозитории GitHub.
