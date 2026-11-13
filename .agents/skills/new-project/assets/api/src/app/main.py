"""HTTP entrypoint. Run with `uv run uvicorn app.main:app --host 127.0.0.1 --port 8000`."""

from app.api.routes import create_app

app = create_app()
