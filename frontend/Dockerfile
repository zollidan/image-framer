FROM oven/bun:1-slim


WORKDIR /code_frontend

COPY . ./code_frontend

RUN bun install

COPY . .

EXPOSE 5173

CMD ["bun", "run", "dev", "--host"]