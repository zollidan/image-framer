FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY . /code

RUN uv sync --frozen --no-cache

CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]