# {{title}} – common targets (run from repo root)
# Usage: make [target]
# Set NO_COLOR=1 (or export NO_COLOR) to disable colors in `make help`.
#
# This file is the three-surface Makefile. Delete the web, API, or database
# targets that the project does not have, and drop them from install, lint, and test.

ifeq ($(NO_COLOR),)
  C_RESET := \033[0m
  C_BOLD := \033[1m
  C_TITLE := \033[1;36m
  C_DIM := \033[2m
  C_SEC_FE := \033[1;33m
  C_SEC_BE := \033[1;35m
  C_SEC_PG := \033[1;32m
else
  C_RESET :=
  C_BOLD :=
  C_TITLE :=
  C_DIM :=
  C_SEC_FE :=
  C_SEC_BE :=
  C_SEC_PG :=
endif

CONTAINER_CMD := $(shell docker version >/dev/null 2>&1 && echo docker || echo podman)
COMPOSE := $(CONTAINER_CMD) compose

.DEFAULT_GOAL := help

.PHONY: help install build lint test check
.PHONY: fe-install fe-dev fe-build fe-lint fe-format fe-test
.PHONY: be-install be-dev be-migrate be-lint be-format be-test
.PHONY: storage-up storage-down storage-reset

help:
	@printf '%b\n' "$(C_BOLD)$(C_TITLE){{title}}$(C_RESET) – $(C_BOLD)available targets:$(C_RESET)"
	@printf '\n'
	@printf '%b\n' "  $(C_TITLE)install$(C_RESET)$(C_DIM)        fe-install, then be-install$(C_RESET)"
	@printf '%b\n' "  $(C_TITLE)build$(C_RESET)$(C_DIM)          Build the web app$(C_RESET)"
	@printf '%b\n' "  $(C_TITLE)lint$(C_RESET)$(C_DIM)           Lint web and API$(C_RESET)"
	@printf '%b\n' "  $(C_TITLE)test$(C_RESET)$(C_DIM)           Test web and API$(C_RESET)"
	@printf '%b\n' "  $(C_TITLE)check$(C_RESET)$(C_DIM)          lint, then test. Run after every change$(C_RESET)"
	@printf '\n'
	@printf '%b\n' "$(C_SEC_FE)Web (apps/web):$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_FE)fe-install$(C_RESET)$(C_DIM)   npm install$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_FE)fe-dev$(C_RESET)$(C_DIM)       npm run dev on http://127.0.0.1:3000$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_FE)fe-build$(C_RESET)$(C_DIM)     npm run build$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_FE)fe-lint$(C_RESET)$(C_DIM)      Typecheck and eslint$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_FE)fe-format$(C_RESET)$(C_DIM)    prettier$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_FE)fe-test$(C_RESET)$(C_DIM)      vitest$(C_RESET)"
	@printf '\n'
	@printf '%b\n' "$(C_SEC_BE)API (apps/api):$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_BE)be-install$(C_RESET)$(C_DIM)   uv sync$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_BE)be-dev$(C_RESET)$(C_DIM)       uvicorn with reload on http://127.0.0.1:8000$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_BE)be-migrate$(C_RESET)$(C_DIM)   alembic upgrade head$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_BE)be-lint$(C_RESET)$(C_DIM)      ruff check and ruff format check$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_BE)be-format$(C_RESET)$(C_DIM)    ruff format$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_BE)be-test$(C_RESET)$(C_DIM)      pytest$(C_RESET)"
	@printf '\n'
	@printf '%b\n' "$(C_SEC_PG)Database:$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_PG)storage-up$(C_RESET)$(C_DIM)     Start Postgres on 127.0.0.1:5432$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_PG)storage-down$(C_RESET)$(C_DIM)   Stop this project's Postgres$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_PG)storage-reset$(C_RESET)$(C_DIM)  Recreate the {{db}} database$(C_RESET)"
	@printf '\n'
	@printf '%b\n' "$(C_BOLD)Quick start$(C_RESET)"
	@printf '%b\n' "  $(C_DIM)make$(C_RESET) $(C_TITLE)install$(C_RESET)"
	@printf '%b\n' "  $(C_DIM)make$(C_RESET) $(C_SEC_PG)storage-up$(C_RESET) $(C_DIM)&& make$(C_RESET) $(C_SEC_BE)be-migrate$(C_RESET)"
	@printf '%b\n' "  $(C_DIM)make$(C_RESET) $(C_SEC_BE)be-dev$(C_RESET)$(C_DIM)               # http://127.0.0.1:8000$(C_RESET)"
	@printf '%b\n' "  $(C_DIM)make$(C_RESET) $(C_SEC_FE)fe-dev$(C_RESET)$(C_DIM)               # http://127.0.0.1:3000$(C_RESET)"

install:
	$(MAKE) fe-install
	$(MAKE) be-install

build: fe-build

lint: fe-lint be-lint

test: fe-test be-test

check: lint test

fe-install:
	cd apps/web && npm install

fe-dev:
	@if lsof -ti tcp:3000 -sTCP:LISTEN >/dev/null 2>&1; then \
		echo "Port 3000 is already in use. Stop that process, then run make fe-dev again."; \
		exit 1; \
	fi
	cd apps/web && npm run dev

fe-build:
	cd apps/web && npm run build

fe-lint:
	cd apps/web && npm run typecheck
	cd apps/web && npm run lint

fe-format:
	cd apps/web && npm run format

fe-test:
	cd apps/web && npm test

be-install:
	cd apps/api && uv sync

be-dev:
	@if lsof -ti tcp:8000 -sTCP:LISTEN >/dev/null 2>&1; then \
		echo "Port 8000 is already in use. Stop that process, then run make be-dev again."; \
		exit 1; \
	fi
	cd apps/api && uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

be-migrate:
	cd apps/api && uv run alembic upgrade head

be-lint:
	cd apps/api && uv run ruff check . && uv run ruff format --check .

be-format:
	cd apps/api && uv run ruff check --fix . && uv run ruff format .

be-test:
	cd apps/api && uv run pytest

storage-up:
	$(COMPOSE) up -d --wait

storage-down:
	$(COMPOSE) down

storage-reset:
	$(CONTAINER_CMD) exec {{slug}}-postgres psql -U postgres -v ON_ERROR_STOP=1 -c "DROP DATABASE IF EXISTS {{db}} WITH (FORCE);"
	$(CONTAINER_CMD) exec {{slug}}-postgres psql -U postgres -v ON_ERROR_STOP=1 -c "CREATE DATABASE {{db}} OWNER {{db}};"
	$(CONTAINER_CMD) exec {{slug}}-postgres psql -U postgres -d {{db}} -v ON_ERROR_STOP=1 -c "CREATE SCHEMA IF NOT EXISTS {{db}} AUTHORIZATION {{db}};"
	$(MAKE) be-migrate
