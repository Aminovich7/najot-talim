# RabbitMQ Basics Tester

Super simple Django project for testing RabbitMQ publish/consume basics.

## What it does

- A single web page with a text field and two buttons.
- `Send to Queue` publishes a message to RabbitMQ.
- `Read One Message` pulls one message from the queue and removes it.
- A Django management command runs a long-lived consumer loop for basic worker testing.

## Requirements

- Python 3.11+ recommended
- Docker Desktop, or a local RabbitMQ server

## Quick start

### 1) Start RabbitMQ

Using Docker:

```bash
docker compose up -d rabbitmq
```

RabbitMQ will be available at:

- AMQP: `localhost:5672`
- Management UI: http://localhost:15672

Default credentials:

- username: `guest`
- password: `guest`

### 2) Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Run the web app

No migrations are required for this starter project.

```bash
python manage.py runserver
```

Open:

- http://127.0.0.1:8000/

## How to test RabbitMQ

### Publish a message

1. Open the home page.
2. Type a message.
3. Click `Send to Queue`.
4. The message is published to the queue configured by `RABBITMQ_QUEUE_NAME`.

### Consume one message from the web UI

1. Publish a few messages first.
2. Click `Read One Message`.
3. The oldest message in the queue is fetched and acknowledged.

### Run the background consumer

Start a separate terminal:

```bash
python manage.py consume_messages
```

Then publish messages from the browser. The consumer will print each message to the console.

## Environment variables

All values are optional for local testing.

```text
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/
RABBITMQ_QUEUE_NAME=demo_queue
```

## Project layout

```text
manage.py
requirements.txt
docker-compose.yml
rabbitmq_tester/
messaging/
```

## Notes

- The app uses durable queues and persistent messages.
- The code is intentionally minimal and is meant for local learning, not production use.
