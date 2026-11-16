"""Postgres.

Unset APP_ENV accepts the loopback starter only.
APP_ENV=production requires TLS and refuses the starter password.
"""

import os

import psycopg

_LOOPBACK = {"127.0.0.1", "localhost", "::1"}
_STARTER_PASSWORD = "{{db}}"


def database_url() -> str:
    mode = os.environ.get("APP_ENV", "")
    if mode == "":
        return _local_url()
    if mode == "production":
        return _production_url()
    raise RuntimeError("APP_ENV must be unset or production.")


def _parse(url: str) -> dict[str, str | int | None]:
    normalized = url.replace("postgresql+psycopg://", "postgresql://", 1)
    try:
        return psycopg.conninfo.conninfo_to_dict(normalized)
    except psycopg.ProgrammingError as exc:
        raise RuntimeError("DATABASE_URL is not a PostgreSQL connection URL.") from exc


def _local_url() -> str:
    configured = os.environ.get(
        "DATABASE_URL",
        "postgresql://{{db}}:{{db}}@127.0.0.1:5432/{{db}}",
    )
    url = configured.replace("postgresql+psycopg://", "postgresql://", 1)
    parsed = _parse(url)
    if parsed.get("host") not in _LOOPBACK:
        raise RuntimeError("The database host must be loopback.")
    if parsed.get("hostaddr") not in {None, "127.0.0.1", "::1"}:
        raise RuntimeError("The database address must be loopback.")
    return url


def _production_url() -> str:
    configured = os.environ.get("DATABASE_URL")
    if not configured:
        raise RuntimeError("DATABASE_URL is required when APP_ENV=production.")
    url = configured.replace("postgresql+psycopg://", "postgresql://", 1)
    parsed = _parse(url)
    if parsed.get("password") == _STARTER_PASSWORD:
        raise RuntimeError("The starter database password is refused in production.")
    if parsed.get("sslmode") != "verify-full":
        raise RuntimeError("The database connection must use sslmode=verify-full.")
    return url


def sqlalchemy_url() -> str:
    url = database_url()
    prefix = "postgresql://"
    if not url.startswith(prefix):
        raise RuntimeError("DATABASE_URL must start with postgresql://")
    return "postgresql+psycopg://" + url[len(prefix) :]


def ping() -> None:
    with psycopg.connect(database_url(), connect_timeout=3) as connection:
        connection.execute("SELECT 1")
