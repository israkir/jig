"""HTTP routes."""

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.infrastructure.db import ping


def create_app() -> FastAPI:
    app = FastAPI(title="{{title}}")

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/ready")
    def ready() -> JSONResponse:
        try:
            ping()
        except (psycopg.Error, OSError, RuntimeError):
            return JSONResponse({"status": "unavailable"}, status_code=503)
        return JSONResponse({"status": "ok"})

    return app
