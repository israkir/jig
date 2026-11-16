# Makefile

Run targets from the repository root. `make` with no target prints help. `NO_COLOR=1` clears every color.

## Colors

| Name | Value | Use |
|------|-------|-----|
| `C_RESET` | `\033[0m` | End a span |
| `C_BOLD` | `\033[1m` | Headings |
| `C_TITLE` | `\033[1;36m` | Project name and combined targets |
| `C_DIM` | `\033[2m` | Descriptions |
| `C_SEC_FE` | `\033[1;33m` | Web targets |
| `C_SEC_BE` | `\033[1;35m` | API targets |
| `C_SEC_PG` | `\033[1;32m` | Database targets |

Help lines use `printf '%b\n'`. Each group is a heading, then the targets, then a blank line.

## Targets

Copy a row only when its surface was chosen. Combined targets call the surface targets that exist, web first, then API.

| Target | Surface | Does |
|--------|---------|------|
| `install` | API or web | `fe-install`, then `be-install`. One after the other |
| `build` | Web | `fe-build` |
| `lint` | API or web | `fe-lint`, then `be-lint` |
| `test` | API or web | `fe-test`, then `be-test` |
| `check` | API or web | `lint`, then `test`. The one command an agent runs after every change |
| `fe-install` | Web | `npm install` in `apps/web` |
| `fe-dev` | Web | Stop if port 3000 is in use, then `npm run dev` |
| `fe-build` | Web | `npm run build` |
| `fe-lint` | Web | `typecheck`, then `lint` |
| `fe-format` | Web | `npm run format` |
| `fe-test` | Web | `npm test` |
| `be-install` | API | `uv sync` in `apps/api` |
| `be-dev` | API | Stop if port 8000 is in use, then uvicorn on `127.0.0.1:8000` with reload |
| `be-lint` | API | `ruff check` and `ruff format --check` |
| `be-format` | API | `ruff check --fix` and `ruff format` |
| `be-test` | API | `uv run pytest` |
| `be-migrate` | API and database | `alembic upgrade head` |
| `storage-up` | Database | `compose up -d --wait` |
| `storage-down` | Database | `compose down` for this project's container |
| `storage-reset` | Database | Drop and recreate `{{db}}`, then `be-migrate` when the API exists |

The container runtime is `docker` when `docker version` succeeds, otherwise `podman`. Compose is that runtime plus `compose`.

`storage-down` stops this project's database. It is not a no-op. A no-op belongs only to a later project that shares another repository's database, and the help line says whose database it would stop.

## Help order

1. Project title and "available targets".
2. Combined targets, in title color.
3. Web group, in `C_SEC_FE`, labeled `Web (apps/web)`.
4. API group, in `C_SEC_BE`, labeled `API (apps/api)`.
5. Database group, in `C_SEC_PG`, labeled `Database`.
6. Quick start: `install`, then `storage-up` and `be-migrate` when those exist, then `be-dev` and `fe-dev` on the ports above.

`assets/Makefile` is the three-surface file. Trim it to the surfaces that were chosen.

| Dropped surface | Remove |
|-----------------|--------|
| Web | `build`, every `fe-*` target, the web help group, and `fe-dev` from the quick start. Point `install`, `lint`, and `test` at the API targets only |
| API | Every `be-*` target, the API help group, and `be-dev` from the quick start. Point `install`, `lint`, and `test` at the web targets only. `storage-reset` stops after recreating the schema |
| Database | `storage-up`, `storage-down`, `storage-reset`, `be-migrate`, the database help group, and the `storage-up` quick-start line |

When web and API are both absent, delete `install`, `lint`, `test`, and `check` as well. When the secrets surface is present and those two are absent, `check` is `secrets-scan`.

## Secrets

Add this group only when the secrets surface was chosen. Add `C_SEC_KEY := \033[1;31m` next to the other color variables, and clear it in the `NO_COLOR` branch. Add the names to `.PHONY`. Insert the help lines inside `help`, after the Database group and before Quick start. Add `secrets-scan` to `check`. `check` does not decrypt. `secrets-check`, `secrets-edit`, `secrets-view`, and `secrets-run` do. `secrets-view` prints values. An agent does not run it.

```makefile
	@printf '%b\n' "$(C_SEC_KEY)Secrets:$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_KEY)secrets-scan$(C_RESET)$(C_DIM)       Fail on a plaintext store or an age private key$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_KEY)secrets-check$(C_RESET)$(C_DIM)      Decrypt and print variable names only$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_KEY)secrets-edit$(C_RESET)$(C_DIM)       Edit the local store with sops$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_KEY)secrets-view$(C_RESET)$(C_DIM)       Print decrypted values. Agents do not run this$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_KEY)secrets-updatekeys$(C_RESET)$(C_DIM) Re-key after changing recipients$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_KEY)secrets-recipients$(C_RESET)$(C_DIM) Warn when the local store has one recipient$(C_RESET)"
	@printf '%b\n' "  $(C_SEC_KEY)secrets-run$(C_RESET)$(C_DIM)        Run CMD with the local store in its environment$(C_RESET)"
```

```makefile
secrets-scan:
	python3 infra/secrets/check_store.py
	python3 infra/secrets/test_secret_store.py

secrets-check:
	python3 infra/secrets/export_env.py app --names

secrets-edit:
	SOPS_AGE_KEY_FILE="$${SOPS_AGE_KEY_FILE:-$(HOME)/.config/sops/age/keys.txt}" sops secrets/local.enc.yaml

secrets-view:
	SOPS_AGE_KEY_FILE="$${SOPS_AGE_KEY_FILE:-$(HOME)/.config/sops/age/keys.txt}" sops decrypt secrets/local.enc.yaml

secrets-updatekeys:
	SOPS_AGE_KEY_FILE="$${SOPS_AGE_KEY_FILE:-$(HOME)/.config/sops/age/keys.txt}" sops updatekeys secrets/local.enc.yaml
	@if [ -f secrets/production.enc.yaml ]; then \
		SOPS_AGE_KEY_FILE="$${SOPS_AGE_KEY_FILE:-$(HOME)/.config/sops/age/keys.txt}" sops updatekeys secrets/production.enc.yaml; \
	fi

secrets-recipients:
	python3 infra/secrets/export_env.py --recipients || [ $$? -eq 3 ]

secrets-run:
	python3 infra/secrets/export_env.py app -- $(CMD)
```
