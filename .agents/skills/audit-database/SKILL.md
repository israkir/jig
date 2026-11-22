---
name: audit-database
description: Audits a Postgres schema against the database standard, covering contexts, names, keys, indexes, and migrations. Use when the user asks to check or design a database, including tables, columns, indexes, schemas, or isolation.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity via .agents/skills.
metadata:
  version: "1.1.0"
  category: database
  tags: audit,database,postgres,schema,indexes
---

# Audit the database

The standard is `references/database-contract.md`. Read it before judging a table. Audit the project against it. Do not redesign the project. Cite the contract from `AGENTS.md`. Do not paste the rules into a second style guide or tool-specific rule file.

## New database

`new-project` creates one role, one database, one schema, and `alembic_version_<db>` in `public`. That is the whole scaffold. The first table follows the contract. Reader and requester roles, a second schema, partitions, and retention wait until a second context or a measured table needs them.

Write the `## Database` section in `AGENTS.md` before the first table.

## Existing database

Inventory the live schema and stop. Wait for approval before editing.

### Inventory

Locate migrations, schema SQL, grants, and the Alembic env. Note the engine, the version table, and `search_path`.

```text
CREATE SCHEMA|CREATE TABLE|CREATE INDEX|CREATE UNIQUE INDEX
alembic_version|search_path|version_table
ON DELETE|ON UPDATE
timestamp without|double precision|real |ENUM|varchar|character varying|char(|jsonb|numeric
uuidv7|gen_random_uuid|created_at|updated_at|fetched_at
PRIMARY KEY|REFERENCES
GRANT |CREATE ROLE
```

Open the migration that creates each table. A dump or a generated model is evidence of names. The migration is the authority when they disagree. A `numeric` with no scale, a `jsonb` column a query reads, and a `PRIMARY KEY` or `REFERENCES` on a column line are D7 and D8.

Build this table and stop.

| Rule | Status | Evidence | Proposed change |
|------|--------|----------|-----------------|

Use the rule ids from the reference. A rule that passes still gets a row, with its evidence. A proposed change names the rule it fixes. A rename of a table that already holds rows stays in the table until the user approves it. A project with no database records that under `## Exceptions`.

## Fix the approved rows

Edit only the rows the user approved, in the order the reference lists the rules. A change to a table that already holds rows is a new revision. An applied revision stays as it is. A new index on a serving table is created concurrently, and the plan comparison from the contract is in the revision comment.

Extend the project's migration chain. Do not add a second schema tool.

## Record the contract

Add or update this section in `AGENTS.md`. Create `CLAUDE.md` containing `@AGENTS.md` only when that file is missing.

```markdown
## Database
Database standard: `.agents/skills/audit-database/references/database-contract.md`
Migrations: <path to the Alembic versions, or the schema SQL>
Exceptions:
- <one line each, or "None.">
```

## Verify

Run the project's migration check on a clone when the database is reachable (`alembic upgrade head`, `alembic check`, or the `make` target that wraps them). Report the command and what it printed. When no database is reachable, report the static inventory and say the upgrade was not run.

The audit is unfinished while a failing rule is neither fixed nor recorded under `## Exceptions` in `AGENTS.md`.
