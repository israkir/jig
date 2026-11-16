---
name: audit-source-structure
description: Audits a repository's source tree against the source-structure standard, covering service directories, Python packages, API layers, and the Next.js app. Use when the user asks to check how source is laid out, or where a module, package, layer, or route belongs.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity via .agents/skills.
metadata:
  version: "1.0.0"
  category: dev
  tags: audit,layout,python,fastapi,nextjs
---

# Audit source structure

The standard is `references/source-structure.md`. Read it before judging a file. Audit the project against it. Do not redesign the project. Cite the contract from `AGENTS.md`. Do not paste the rules into a second style guide or tool-specific rule file.

## New project

`new-project` creates `apps/api/src/app` with `domain`, `application`, `infrastructure`, and `api`, and `apps/web/src/app` with `lib`. That is the whole scaffold. The next module follows the contract.

Write the `## Source` section in `AGENTS.md` before adding a module that the scaffold does not already have.

## Existing project

Inventory the tree and stop. Wait for approval before editing.

### Inventory

Locate `apps/`, `packages/`, a root `src/`, and the web `src/app`. Note the Python import name and whether tests sit beside `src/`.

```text
apps/api|apps/web|apps/backend|apps/frontend|packages/
src/app|alembic/|migrations/
domain|application|infrastructure|routers/|services/|models/
from fastapi|from sqlalchemy|HTTPException|os\.environ|datetime\.now
"use client"|fetch\(|src/app/api|src/features|src/components
```

Open the composition root (`main.py` or the FastAPI constructor) and one route. A directory name is evidence. The imports are the authority for which layer a module belongs to.

Build this table and stop.

| Rule | Status | Evidence | Proposed change |
|------|--------|----------|-----------------|

Use the rule ids from the reference. A rule that passes still gets a row, with its evidence. A proposed change names the rule it fixes. A rename of `apps/backend`, `apps/frontend`, or a flat `app/` package stays in the table until the user approves it. A project with no API and no web app records that under `## Exceptions`.

## Fix the approved rows

Edit only the rows the user approved, in the order the reference lists the rules. Move a module into the package the contract names. Leave its behaviour as it is. A new directory under `src/` that the contract does not list waits for an exception in `AGENTS.md`.

Extend the tree that exists. Do not add a second service directory beside one that already serves that role.

## Record the contract

Add or update this section in `AGENTS.md`. Create `CLAUDE.md` containing `@AGENTS.md` only when that file is missing.

```markdown
## Source
Source structure: `.agents/skills/audit-source-structure/references/source-structure.md`
API: <apps/api, or "None.">
Web: <apps/web, or "None.">
Exceptions:
- <one line each, or "None.">
```

## Verify

When a Python module moved, run the project's lint and type check (`uv run ruff check`, `uv run mypy`, or the `make` target that wraps them) and the tests for that package. When a TypeScript module moved, run the project's type check and unit tests. Report the commands and what they printed. When the inventory found no move to make, say that no check was run.

The audit is unfinished while a failing rule is neither fixed nor recorded under `## Exceptions` in `AGENTS.md`.
