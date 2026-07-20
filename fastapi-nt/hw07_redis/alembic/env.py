import sys
import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# loyiha ildizini path'ga qo'shamiz, shunda "app" paketini import qila olamiz
sys.path.append(os.getcwd())

from app.core.config import settings
from app.db.base import Base
from app.models import User, Post, Comment, Like  # noqa: F401  (metadata to'liq bo'lishi uchun barchasi import qilinishi shart)

# Alembic Config obyekti — .ini fayldagi qiymatlarga kirish imkonini beradi
config = context.config

# DATABASE_URL'ni .env dan olib, alembic konfiguratsiyasiga qo'yamiz
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging sozlamalarini ishga tushiramiz (agar .ini faylda mavjud bo'lsa)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Modellarimizning metadata'si — Alembic shu orqali jadvallarni "ko'radi"
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    'Offline' rejim — haqiqiy DB ulanishisiz, faqat SQL skript generatsiya qiladi.
    Odatda kamdan-kam ishlatiladi, lekin Alembic standarti sifatida qoldiramiz.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """
    Haqiqiy migratsiya jarayoni — sync connection ustida ishlaydi
    (async connection ichida chaqiriladi, quyida ko'rasiz).
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    'Online' rejim — async engine orqali haqiqiy DB'ga ulanib, migratsiyani bajaradi.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Bu funksiya Alembic tomonidan chaqiriladi (masalan, 'alembic upgrade head' buyrug'ida).
    Ichida asyncio.run() orqali yuqoridagi async funksiyani ishga tushiramiz.
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()