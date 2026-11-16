"""Alembic environment.

The version table is alembic_version_{{db}} in public.
The connection pins search_path=public so a role named {{db}} does not put
that schema first on the path and hide it from Alembic's comparison.
Objects are created as {{db}}.<name>.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

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
    connectable = create_engine(
        sqlalchemy_url(),
        poolclass=pool.NullPool,
        connect_args={"options": "-c search_path=public"},
    )
    with connectable.connect() as connection:
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
