# Layout

One repository. Processes run on the host. Postgres runs in a container and listens on `127.0.0.1` only.

## Tokens

| Token | Rule | Example for "Northwind" |
|-------|------|-------------------------|
| `{{slug}}` | Lowercase letters, digits, and hyphens. Used in paths, the compose project, and the container name | `northwind` |
| `{{db}}` | `{{slug}}` with hyphens replaced by underscores. Must match `^[a-z][a-z0-9_]*$`. Database name, role, and schema | `northwind` |
| `{{title}}` | The name a person reads | `Northwind` |

The database password in the starter is `{{db}}`. It is for the loopback container only.

## Tree

```
Makefile
AGENTS.md
CLAUDE.md          @AGENTS.md
README.md          warns which tools a clone needs
compose.yaml       database surface
postgres/initdb/   database surface
apps/api/          API surface
apps/web/          web surface
.sops.yaml         secrets surface
.env.example       secrets surface, non-secret settings only
secrets/           secrets surface
infra/secrets/     secrets surface
```

Copy only the rows for the chosen surfaces.

| Surface | From | To |
|---------|------|----|
| Any | `assets/Makefile` | `Makefile` |
| Any | `assets/AGENTS.md` | `AGENTS.md` |
| Any | `assets/CLAUDE.md` | `CLAUDE.md` |
| Any | `assets/README.md` | `README.md` |
| Any | `assets/gitignore` | `.gitignore` |
| API | `assets/api/` | `apps/api/` |
| Web | `assets/web/` | `apps/web/` |
| Database | `assets/compose.yaml` | `compose.yaml` |
| Database | `assets/postgres/` | `postgres/` |
| Secrets | `assets/secrets/sops.yaml` | `.sops.yaml` |
| Secrets | `assets/secrets/env.example` | `.env.example` |
| Secrets | `assets/secrets/README.md` | `secrets/README.md` |
| Secrets | `assets/secrets/infra/` | `infra/secrets/` |

When the API is copied without the database, delete `apps/api/alembic.ini`, `apps/api/alembic/`, and `apps/api/src/app/infrastructure/db.py`. In `apps/api/pyproject.toml`, delete the `# surface: database` block. In `apps/api/src/app/api/routes.py`, delete the `psycopg` import, the `JSONResponse` import, the `ping` import, and `ready`. Leave `README.md` as copied. It tells a clone which tools to install from the directories that exist.

## API

Python 3.12 or newer. uv installs the project. The distribution name is `{{slug}}`. The import package is `app`, and it lives in `src/` so tests import the installed package rather than a folder sitting next to them.

```
apps/api/src/app/domain            pure rules, no framework and no IO
apps/api/src/app/application       use cases
apps/api/src/app/infrastructure    Postgres and other IO
apps/api/src/app/api               HTTP
apps/api/tests
apps/api/alembic                   only with the database surface
```

`GET /api/health` returns `{"status": "ok"}`. With the database surface, `GET /api/ready` runs `SELECT 1` and answers 503 when Postgres cannot be reached. The app and Alembic both read `DATABASE_URL`, or `postgresql://{{db}}:{{db}}@127.0.0.1:5432/{{db}}`. A host other than loopback is refused. The migration connection pins `search_path=public`. Tables are created as `{{db}}.<table>`. The version table stays `alembic_version_{{db}}` in `public`.

Ruff line length is 100. Mypy checks `app`. Pytest collects `tests/`. Schema changes after the first revision go through Alembic.

## Web

Next.js App Router, React 19, TypeScript. npm installs it. The dev server binds `127.0.0.1:3000`. Configuration stays at `apps/web/`. Application code stays in `src/`. The UI font is IBM Plex Sans, and the monospace font is IBM Plex Mono.

```
apps/web/src/app/layout.tsx
apps/web/src/app/page.tsx
apps/web/src/app/globals.css
apps/web/src/app/api/          route handlers, including GET /api/health
apps/web/src/lib/
```

`package.json` sets `engines.node` to 20.9 or newer. A browser call goes to a route handler under `src/app/api`. It does not call port 8000. Add a handler there when the web app needs the API.

A visible time states its kind in sentence case. Unless the time is the user's own action, the label also states the source, for example "As of 14:32 · Exchange" or "Synced 2m ago · This API". The page states one provenance. A row adds its own time only when its kind or its source differs from that page.

## Database

One Postgres 18 container, one role, one database, and one schema. The role, database, and schema are all `{{db}}`. The init script runs on an empty volume. `storage-reset` recreates the database on a volume that already has data.

The schema standard is `../audit-database/references/database-contract.md`. Read it before adding a table. Cite it from the project's `AGENTS.md`. Do not paste it.

Objects are schema-qualified. The migration connection pins `search_path=public`. The version table is `alembic_version_{{db}}` in `public`. Bind `127.0.0.1:5432` only.

Add Redis when the user asks for a queue, and a document store when they ask for documents. A fast-growing time series uses the monthly range partitions in the database standard. TimescaleDB is an exception recorded in that project's `AGENTS.md`. The image for that exception is `docker.io/timescale/timescaledb:2.31.0-pg18`.

## Secrets

Copy this surface only when the user asks for secrets, production deployment, or SOPS. A new project that names no surface does not get it.

The standard is `../audit-secrets/references/secrets-contract.md`. Cite it from the project's `AGENTS.md`. Do not paste it.

SOPS + age holds real credentials. The loopback starter password stays in Compose and is not a store entry. Local and production are different files: `secrets/local.enc.yaml` and `secrets/production.enc.yaml`. `.sops.yaml` gives them different recipients. Do not generate a private key. Do not commit a decrypted store.

Append the lines in `assets/secrets/gitignore.lines` to `.gitignore` when they are absent. Add the Secrets targets from `references/makefile.md`, and add `secrets-scan` to `check`.

When the API and the database are both present, replace `apps/api/src/app/infrastructure/db.py` with `assets/secrets/db.py` and copy `assets/secrets/test_database_url.py` to `apps/api/tests/test_database_url.py`. Keep `DATABASE_URL` in the schema. When the database surface is absent, remove `DATABASE_URL` from `OWN` in `infra/secrets/secret_store.py`.

## AGENTS.md

`assets/AGENTS.md` is the starter. Set `{{surfaces}}` to the surfaces that were created. Add these rules when the surface exists:

- API: domain code imports no framework and does no IO. HTTP lives in `app/api`. Postgres lives in `app/infrastructure`. Ruff line length is 100, and `uv run mypy` stays clean for `app`. The API listens on `127.0.0.1:8000`. A timestamp field's name states the moment: event, source publication, time this API served the payload, or a user action.
- Web: the web app listens on `127.0.0.1:3000`. Browser calls go through this app's route handlers. A visible time states its kind and, unless it is the user's own action, its source.
- Database: cite `.agents/skills/audit-database/references/database-contract.md`. The database name, role, and schema are `{{db}}` on `127.0.0.1:5432`. A host other than loopback is refused. Objects are schema-qualified. The migration connection pins `search_path=public`. The version table is `alembic_version_{{db}}` in `public`. An applied revision is not edited.
- Secrets: under Verify, cite `.agents/skills/audit-secrets/references/secrets-contract.md`. `APP_ENV` is unset or `production`. Unset keeps the loopback starter password, which is not in the store. `production` refuses that password, a missing `DATABASE_URL`, and a database URL without `sslmode=verify-full`. Agents do not read the age key, decrypt the store, or print secret values.

Do not copy this reference into `AGENTS.md`.
