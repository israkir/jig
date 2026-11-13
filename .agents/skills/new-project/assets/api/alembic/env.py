"""Alembic environment. The version table is alembic_version_{{db}} in public."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool, text

from app.infrastructure.db import sqlalchemy_url

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", sqlalchemy_url())

VERSION_TABLE = "alembic_version_{{db}}"


def run_migrations_offline() -> None:
    context.configure(
        url=sqlalchemy_url(),
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table=VERSION_TABLE,
        version_table_schema="public",
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(sqlalchemy_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        connection.execute(text("SET search_path TO {{db}}, public"))
        context.configure(
            connection=connection,
            version_table=VERSION_TABLE,
            version_table_schema="public",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
