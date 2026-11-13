---
name: new-project
description: Scaffolds a minimal working API, web app, database, or any combination of them, with the shared layout and the colored Makefile, then links the project so every agent can read the jig skills. Use when the user asks to start a project or to add one of those surfaces.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity via .agents/skills.
metadata:
  version: "1.4.0"
  category: dev
  tags: project,scaffold,makefile,fastapi,nextjs,postgres
---

# New project

Scaffold only the surfaces the user asked for. The files to copy are in this skill. Read `references/layout.md` and `references/makefile.md` before writing anything. Do not paste those references into the project's README.

## Surfaces

Use what the user named.

| They asked for | Copy |
|----------------|------|
| A new project, with no surface named | API, web, and database |
| API, backend, or FastAPI | API |
| Frontend, web, or Next.js | Web |
| Database or Postgres | Database |

A named subset is the whole job. Do not add a surface they left out.

## Names

Take the project name from the user. Derive the three tokens in `references/layout.md`: `{{slug}}`, `{{db}}`, and `{{title}}`. Stop and ask once when the name would not make a legal database identifier.

## New repository

The repository has none of these surfaces yet.

1. Copy the files for each chosen surface from `assets/`. The map is in `references/layout.md`.
2. Replace `{{slug}}`, `{{db}}`, and `{{title}}` in every copied file.
3. Copy `assets/Makefile` to `Makefile`. Remove every target the project does not have, using the trim list in `references/makefile.md`.
4. Write `AGENTS.md` from `assets/AGENTS.md` and `CLAUDE.md` from `assets/CLAUDE.md`. Replace `{{surfaces}}` with the chosen surfaces. Keep the Commands, Verify, Conventions, and Exceptions sections.
5. Copy `assets/gitignore` to `.gitignore` and `assets/README.md` to `README.md`.
6. `chmod +x postgres/initdb/00-init-database.sh` when the database surface is included.

## Existing repository

Inventory first. Add a missing surface from the same assets. Keep a working target, app, or compose file. Add the missing help lines and recipes from `references/makefile.md`. Record the surfaces in `AGENTS.md`.

## Link the project

Resolve this skill's directory to its real path. The jig repository is the one that contains `.agents/skills`. Run `<jig>/bin/jig link <project>`. That writes symlinks so Cursor, Claude Code, Codex, and Antigravity in this project read the same skills. An `audit-` skill is how the project is checked later.

## Verify

From the repository root, run `make help` and confirm only the chosen surfaces are listed. `make check` is the single verify command; run it last.

- API: `cd apps/api && uv sync && uv run pytest`
- Web: `cd apps/web && npm install && npm run typecheck && npm test`
- Database, when the API is present: `make storage-up && make be-migrate`

Report the commands you ran and any failure. Do not describe a command you did not run as done.
