# Source structure

This file is the source-structure standard. A new project follows it from the first module. An existing tree is audited against it. The layout is the one the Copinance family uses for a service and a library. Where the repositories disagree, the form here is the one the language or the framework specifies. A project cites this path from `AGENTS.md` and lists exceptions. Do not paste these rules into a second style guide.

## S1. Services and libraries

Application code lives in one place.

| Kind | Path | Import name |
|------|------|-------------|
| HTTP API | `apps/api` | `app` |
| Web app | `apps/web` | the TypeScript project in that directory |
| Library another service imports | `packages/<name>` | the distribution name, hyphens replaced by underscores |
| Repository that is only a library | `src/<import_name>` and `tests/` at the root | the same import name |

`apps/api` and `apps/web` are the service directories. A second process with its own entrypoint and its own dependencies is a second directory under `apps/`. A background job of a service stays in that service.

A library has its own `pyproject.toml`, `src/<import_name>/`, and `tests/`. The import name matches `^[a-z][a-z0-9_]*$`.

`infra/` holds process wiring. `docs/` holds documents. `scripts/` holds scripts. Application modules stay in `apps/` or `packages/`.

## S2. Python package

Production code lives in `src/<import_name>/`. Tests live in `tests/` next to `src/` and import the installed package.

```
apps/api/pyproject.toml
apps/api/src/app/
apps/api/tests/
apps/api/alembic/                 application that has a database
packages/<name>/pyproject.toml
packages/<name>/src/<import_name>/
packages/<name>/tests/
```

An application's Alembic tree is `alembic/` beside that app's `pyproject.toml`, which is the layout `alembic init` writes. A library that owns a schema keeps its migrations inside the import package, so they install with the library.

Modules, functions, and variables are `snake_case`. Classes are `PascalCase`. Constants are `UPPER_SNAKE`. A repository class is `Postgres<Thing>Repository`. A use case is `<Thing>Service`.

## S3. API layers

An HTTP service has four packages under `src/app/`. Dependencies point inward.

```
api → application → domain ← infrastructure
```

| Package | Holds | Stays out |
|---------|-------|-----------|
| `domain` | Rules, values, and the ports those rules call | FastAPI, SQLAlchemy, network, files, `os.environ`, `datetime.now()` |
| `application` | Use cases. They call domain and ports | SQL, HTTP clients, route declarations |
| `infrastructure` | Adapters that implement ports | Route declarations, response models |
| `api` | Routers, `Depends()` providers, request and response models | Business rules, queries |

`main.py` is the composition root. It is the module that may import all four packages. It builds the FastAPI app, constructs adapters, and maps domain errors to HTTP responses. Domain and application code does not raise `HTTPException`.

`config.py` is the one settings object, using pydantic-settings. Other modules do not read `os.environ`.

A port the domain calls lives in `domain/ports.py`. A port only a use case calls lives in `application/`. The class that implements a port lives in `infrastructure/`.

A route module validates input, calls one use case, and serializes the result. The route receives adapters through `Depends()`. It does not construct a repository. One resource is one module under `app/api/`. A service that still has a single module may keep it in `app/api/routes.py`. Pydantic models of the wire stay in `app/api/`.

A domain value is a dataclass or a pydantic model that does not import FastAPI. A clock the domain needs is an argument or a port. The domain receives a date.

A library does not gain empty layer packages. When a library has adapters, pure modules still do not import them. Its composition root wires the adapters.

| Change | Place |
|--------|-------|
| A rule, a calculation, a closed set | `domain/` |
| A use case | `application/`, class `<Thing>Service` |
| SQL, an HTTP client, the filesystem | `infrastructure/` |
| A route, a request model, a response model | `app/api/` |
| A setting | `config.py`, and `.env.example` when the project has one |
| A job of this service | `application/` for the job, `infrastructure/` for its IO |

## S4. Web app

Next.js App Router. React components. Configuration stays at `apps/web/`. Application code stays in `src/`, which keeps it apart from `package.json` and `next.config`.

```
apps/web/src/app/                         routes
apps/web/src/app/<route>/page.tsx
apps/web/src/app/<route>/_components/     this route only
apps/web/src/app/<route>/_lib/            this route only
apps/web/src/app/api/<name>/route.ts      route handlers
apps/web/src/components/                  UI used by more than one route
apps/web/src/lib/                         modules used by more than one route
apps/web/src/features/<name>/             a domain used by more than one route
```

A route segment and a special file use the names Next.js requires: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `route.ts`, `template.tsx`, `default.tsx`. A group that must not change the URL is `(name)`. A folder the router must ignore starts with `_`.

Every other file is kebab-case. A component's export is `PascalCase`. A hook's export is `useCamelCase`, and its file is `use-<name>.ts`. Named exports, except the default export Next.js requires on a special file.

`"use client"` is the first statement of a file that uses state, effects, or a browser API. A page, a layout, and any module that does not need those stay server components.

A domain that one route uses stays under that route, in `_components` and `_lib`. It moves to `src/features/<name>/` when a second route imports it. UI that a second route needs and that is not a domain moves to `src/components/`. A function that a second route needs moves to `src/lib/`.

The directories directly under `src/` are `app`, `components`, `lib`, `features`, and `stores`. `features/` is present when one domain is used by more than one route. `stores/` is present when UI state is read by more than one route, and it keeps no copy of data the server already returned. Any other directory directly under `src/` is an exception in `AGENTS.md`.

Client code calls a route handler under `src/app/api`, through one module, `src/lib/api.ts`. The route handler calls the API. A component leaves `fetch` to that module.

A function with branches lives in `lib/` or in the route's `_lib/`, with its test beside it (`format-money.ts`, `format-money.test.ts`). The component file declares UI.

| Change | Place |
|--------|-------|
| A page | `src/app/<route>/page.tsx` |
| UI only that page uses | `src/app/<route>/_components/` |
| A function only that page uses | `src/app/<route>/_lib/` |
| UI two routes use | `src/components/` |
| A function two routes use, and the fetch client | `src/lib/` |
| A domain two routes use | `src/features/<name>/` |
| The HTTP handler the browser calls | `src/app/api/<name>/route.ts` |

## S5. Tests

Python tests are `tests/test_*.py` next to `src/`, outside the import package. TypeScript tests are `*.test.ts` beside the module they guard. An end-to-end suite is `e2e/`. Application code imports nothing from it.
