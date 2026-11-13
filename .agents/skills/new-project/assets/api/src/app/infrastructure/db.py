"""Postgres. The host must be loopback."""

import os

import psycopg

_LOOPBACK = {"127.0.0.1", "localhost", "::1"}


def database_url() -> str:
    configured = os.environ.get(
        "DATABASE_URL",
        "postgresql://{{db}}:{{db}}@127.0.0.1:5432/{{db}}",
    )
    url = configured.replace("postgresql+psycopg://", "postgresql://", 1)
    try:
        parsed = psycopg.conninfo.conninfo_to_dict(url)
    except psycopg.ProgrammingError as exc:
        raise RuntimeError("DATABASE_URL is not a PostgreSQL connection URL.") from exc
    if parsed.get("host") not in _LOOPBACK:
        raise RuntimeError("The database host must be loopback.")
    if parsed.get("hostaddr") not in {None, "127.0.0.1", "::1"}:
        raise RuntimeError("The database address must be loopback.")
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
