---
name: audit-secrets
description: Audits a project's secrets against the SOPS and age standard, including the store schema, production recipients, and agent access. Use when the user asks to check, tidy, or improve secrets management.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity via .agents/skills.
metadata:
  version: "1.0.0"
  category: dev
  tags: audit,secrets,sops,age
---

# Audit secrets

The standard is `references/secrets-contract.md`. Read it before judging anything. Audit the project against it. Do not redesign the project. Do not decrypt a store, read an age key, or print a secret value.

## Inventory

List what exists. Open the schema, `.sops.yaml`, `AGENTS.md`, and the database URL code. Do not run `sops decrypt`, `make secrets-view`, or the export helper in front of a command.

```text
.sops.yaml  secrets/  infra/secrets/  .env  .env.example  .gitignore
AGENTS.md  Makefile  apps/api/src/app/infrastructure/db.py
```

Recipient lines inside an `*.enc.yaml` are plaintext metadata. Count those. Do not decrypt the values above them.

Build this table and stop. Wait for approval before editing.

| Rule | Status | Evidence | Proposed change |
|------|--------|----------|-----------------|

Use the rule ids from the reference. A rule that passes still gets a row, with its evidence. A proposed change names the rule it fixes. A project that has no secrets to keep records that under `## Exceptions` instead of gaining an empty store.

## Fix the approved rows

Edit only the rows the user approved, in the order the reference lists the rules. Keep the schema as the one list of names. Do not write a secret into a file that is committed decrypted.

## Record the contract

Add or update this line under `## Verify` in `AGENTS.md`. Create `CLAUDE.md` containing `@AGENTS.md` only when that file is missing.

```markdown
Secrets: `.agents/skills/audit-secrets/references/secrets-contract.md`
```

A deploy that cannot follow a rule yet is one line under `## Exceptions`.

## Verify

Run `make check` after the approved edits. Report the command and what it printed. The check fails on a plaintext value in a committed store and on an age private key in the tree.

The audit is unfinished while a failing rule is neither fixed nor recorded under `## Exceptions` in `AGENTS.md`.
