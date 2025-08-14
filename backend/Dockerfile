FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY . /code

RUN uv sync --frozen --no-cache

EXPOSE 80
