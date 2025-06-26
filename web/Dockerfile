FROM oven/bun:alpine as build

WORKDIR /app

COPY . .

RUN bun install

EXPOSE 3457

CMD ["bun", "run", "prod"]