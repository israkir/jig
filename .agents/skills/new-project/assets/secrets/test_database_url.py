"""Database URL modes."""

import pytest

from app.infrastructure.db import database_url


def test_local_refuses_a_non_loopback_host(monkeypatch: pytest.MonkeyPatch) -> None:
    """Guards: a non-loopback host is accepted while APP_ENV is unset."""
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://{{db}}:{{db}}@db.example:5432/{{db}}")
    with pytest.raises(RuntimeError, match="loopback"):
        database_url()


def test_production_refuses_a_missing_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """Guards: production boots when DATABASE_URL is missing."""
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="required"):
        database_url()


def test_production_refuses_the_starter_password(monkeypatch: pytest.MonkeyPatch) -> None:
    """Guards: production accepts the starter password."""
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://{{db}}:{{db}}@db.example:5432/{{db}}?sslmode=verify-full",
    )
    with pytest.raises(RuntimeError, match="starter"):
        database_url()


def test_production_refuses_a_database_url_without_verify_full(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Guards: production accepts a database URL without sslmode=verify-full."""
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://{{db}}:not-the-starter@db.example:5432/{{db}}",
    )
    with pytest.raises(RuntimeError, match="verify-full"):
        database_url()


def test_a_misspelled_app_env_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """Guards: APP_ENV=prod is treated as local and accepts a remote host."""
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://{{db}}:not-the-starter@db.example:5432/{{db}}",
    )
    with pytest.raises(RuntimeError, match="APP_ENV"):
        database_url()
