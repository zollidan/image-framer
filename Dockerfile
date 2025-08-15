FROM oven/bun:latest AS frontend-builder

WORKDIR /code_frontend

COPY /frontend /code_frontend

RUN bun install --frozen-lockfile
RUN bun run build

FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY . /code

COPY --from=frontend-builder /code_frontend/dist ./static

RUN uv sync --frozen --no-cache

EXPOSE 8000

CMD [ "uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0"]