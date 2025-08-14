FROM oven/bun:latest

WORKDIR /code_frontend

COPY . /code_frontend

RUN bun install --frozen-lockfile
RUN bun add serve
RUN bun run build

EXPOSE 3000
