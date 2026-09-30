# Connexa

The backend for a social network, built with FastAPI and async SQLAlchemy.

**Status: early development.** The application skeleton, settings, async database session, migrations, Docker setup and user registration are in place.

## Stack

Python · FastAPI · SQLAlchemy 2 (async) with asyncpg · PostgreSQL · Alembic · pydantic-settings · Argon2 password hashing · Docker

## Project layout

| Path | What |
|---|---|
| `app/main.py` | FastAPI application and health endpoints |
| `app/core/config.py` | settings loaded from `.env` |
| `app/db/` | async engine, session and the `get_db` dependency |
| `app/common/security.py` | password hashing |
| `app/users/` | user model, schemas, repository, service and router (layered: router → service → repository) |
| `alembic/` | database migrations |

## Running with Docker

```bash
cp .env.example .env
docker compose up --build
```

Create the database tables (first run, and after pulling new migrations):

```bash
docker compose exec api alembic upgrade head
```

The API runs at http://localhost:8000; interactive docs are at http://localhost:8000/docs.

| Endpoint | What |
|---|---|
| `GET /` | welcome message |
| `GET /health` | service status |
| `GET /db-check` | confirms the database connection |
| `POST /auth/register` | create an account (email, username, full name, password); rejects duplicate emails and usernames |

## Configuration

| Variable | Purpose |
|---|---|
| `APP_NAME`, `API_VERSION` | shown in the API docs |
| `DEBUG` | debug mode |
| `DATABASE_URL` | async PostgreSQL URL (`postgresql+asyncpg://…`) |
