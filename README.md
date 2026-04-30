# LunaMKK

FastAPI-сервис для создания и проверки платежей. Проект использует PostgreSQL,
RabbitMQ, Alembic, фоновую отправку событий из outbox и отдельный consumer worker
для обработки платежных событий.

## Требования

- Python 3.12
- Docker и Docker Compose
- PostgreSQL 15
- RabbitMQ 4.x

## Переменные окружения

Создайте файл `.env` в корне проекта:

```env
NAME_DB=lunamkk
USERNAME_DB=postgres
PASSWORD_DB=postgres
HOST_DB=localhost
PORT_DB=5432
API_KEY=dev-api-key
RABBIT_URL=amqp://guest:guest@localhost:5672/
OUTBOX_RETRIES=3
```

Если приложение запускается внутри Docker Compose, для подключения к сервисам
используйте имена контейнеров:

```env
HOST_DB=pg
RABBIT_URL=amqp://guest:guest@rabbit:5672/
```

## Быстрый запуск локально

Запустите docker compose:

```bash
docker compose up --build api
```

API будет доступно по адресу:

```text
http://localhost:8000
```

RabbitMQ Management UI:

```text
http://localhost:15672
```

Логин и пароль по умолчанию: `michael` / `michael`.

## Проверка API

Все эндпоинты защищены заголовком `X-API-Key`. Для создания платежа также нужен
заголовок `Idempotency-Key`.

### Healthcheck

```bash
curl -X GET "http://localhost:8000/health/live" \
  -H "X-API-Key: dev-api-key"
```

Ответ:

```json
{
  "status": "alive"
}
```

### Создать платеж

```bash
curl -X POST "http://localhost:8000/api/v1/payments/" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-api-key" \
  -H "Idempotency-Key: payment-001" \
  -d '{
    "amount": 1500,
    "currency": "RUB",
    "description": "Test payment",
    "meta": {
      "order_id": "order-123"
    },
    "webhook_url": "https://example.com/webhook"
  }'
```

Пример ответа:

```json
{
  "id": 1,
  "status": "PENDING",
  "created_at": "2026-04-30T12:00:00Z",
  "is_new": true
}
```

Повторный запрос с тем же `Idempotency-Key` вернет уже созданный платеж с
`is_new: false`.

Доступные валюты:

```text
USD, EUR, RUB
```

### Получить платеж по ID

```bash
curl -X GET "http://localhost:8000/api/v1/payments/1" \
  -H "X-API-Key: dev-api-key"
```

Пример ответа:

```json
{
  "id": 1,
  "idempotency_key": "payment-001",
  "amount": 1500,
  "currency": "RUB",
  "description": "Test payment",
  "meta": {
    "order_id": "order-123"
  },
  "webhook_url": "https://example.com/webhook"
}
```

## Полезные команды

Создать новую Alembic-миграцию:

```bash
alembic revision --autogenerate -m "migration name"
```

Откатить последнюю миграцию:

```bash
alembic downgrade -1
```

Посмотреть логи сервисов:

```bash
docker compose logs -f
```

Посмотреть логи конкретного сервиса:

```bash
docker compose logs -f api
```
