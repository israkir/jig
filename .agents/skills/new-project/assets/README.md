# {{title}}

Run `make help`.

This repository uses one stack. Install the tools for the parts that are present. A missing tool means those targets cannot run. A different language, framework, or database is an exception recorded in `AGENTS.md`.

## Platform

| Present here | Install |
|--------------|---------|
| `Makefile` | GNU Make |
| `apps/api` | Python 3.12 or newer, and uv |
| `apps/web` | Node.js 20.9 or newer, and the npm shipped with it |
| `compose.yaml` | Docker or Podman. Postgres 18 is the image in that file, not a host install |

## Libraries

`make install` installs the libraries. The floors are the newest set that install together. The package manager may select a newer release above a floor.

| Present here | Where the versions live |
|--------------|-------------------------|
| `apps/api` | `apps/api/pyproject.toml` — FastAPI, Pydantic, uvicorn. Dev tools are httpx2, mypy, pytest, and Ruff |
| `apps/api` and `compose.yaml` | the same file — Alembic, psycopg, and SQLAlchemy |
| `apps/web` | `apps/web/package.json` — Next.js, React, TypeScript, ESLint, Vitest, and Prettier |
