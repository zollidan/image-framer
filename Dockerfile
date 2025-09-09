# Multi-stage build для объединения всех компонентов приложения

# Стадия 1: Сборка backend
FROM python:3.13-slim AS backend-build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /backend
COPY backend/ .
RUN uv sync --frozen --no-cache

# Стадия 2: Сборка frontend
FROM oven/bun:1 AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/bun.lock ./
RUN bun install --frozen-lockfile
COPY frontend/ .
ENV NODE_ENV=production
RUN bun run build

# Стадия 3: Финальный образ с nginx и всеми компонентами
FROM nginx:1.25.3-alpine-slim AS final

# Установка Python и необходимых зависимостей для backend
RUN apk add --no-cache python3 py3-pip supervisor

# Копирование backend
COPY --from=backend-build /backend /app/backend
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Копирование собранного frontend в nginx
COPY --from=frontend-build /frontend/dist /usr/share/nginx/html

# Создание конфигурации nginx для объединенного приложения
RUN rm /etc/nginx/conf.d/default.conf
COPY <<'EOF' /etc/nginx/conf.d/default.conf
server {
    listen 80;
    server_name localhost;
    
    # Увеличиваем лимит размера запроса для загрузки изображений
    client_max_body_size 50M;
    
    # Frontend - статические файлы
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
        
        add_header X-Frame-Options SAMEORIGIN;
        add_header X-Content-Type-Options nosniff;
    }
    
    # Backend API
    location ^~ /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        proxy_intercept_errors on;
        error_page 502 503 504 = @backend_fallback;


        proxy_buffering off;
    }
    
    # Fallback для случаев, когда backend недоступен
    location @backend_fallback {
        return 503 "Backend service temporarily unavailable";
        add_header Content-Type text/plain;
    }
    
    # Статические файлы с кешированием
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        root /usr/share/nginx/html;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
    
    access_log /var/log/nginx/access.log combined;
    error_log /var/log/nginx/error.log debug;
}
EOF

# Создание конфигурации supervisor для запуска backend и nginx
COPY <<'EOF' /etc/supervisord.conf
[supervisord]
nodaemon=true
user=root
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid

[program:backend]
command=uv run fastapi run app/main.py --host 127.0.0.1 --port 8000
directory=/app/backend
autostart=true
autorestart=true
stderr_logfile=/var/log/backend.err.log
stdout_logfile=/var/log/backend.out.log
environment=ENV=production
startretries=3
startsecs=10

[program:nginx]
command=nginx -g "daemon off;"
autostart=true
autorestart=true
stderr_logfile=/var/log/nginx.err.log
stdout_logfile=/var/log/nginx.out.log
EOF

# Создание директорий для логов
RUN mkdir -p /var/log/supervisor

EXPOSE 80

CMD ["supervisord", "-c", "/etc/supervisord.conf"]