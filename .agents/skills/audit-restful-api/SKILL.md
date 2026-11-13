---
name: audit-restful-api
description: Audits an existing HTTP API against the REST standard. Use when the user asks to check or audit an API, including its routes, verbs, status codes, problem details, or hypermedia.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity via .agents/skills.
metadata:
  version: "2.1.0"
  category: api
  tags: audit,rest,api,http,openapi,hypermedia
---

# Audit a RESTful API

The standard is `references/rest-rules.md`. Read it before judging a route. The application's OpenAPI document is the live contract for that repo. Cite the standard from `AGENTS.md`. Do not paste the rules into a second style guide or tool-specific rule file.

Adapt examples to the stack. Record every deviation in `AGENTS.md` under `## API`.

## New API

There is no published client yet. Apply the standard as you add routes. Default to Level 2 for an internal service and Level 3 for a client-facing API, as the reference defines. Write the `## API` section in `AGENTS.md` before the first route.

## Existing API

Audit the project against the standard. Do not redesign it.

### Inventory

Locate routers, controllers, OpenAPI or Swagger files, and any gateway or BFF. Note the framework and the existing representation style.

Search the tree for route declarations, RPC-style names, hypermedia, caching headers, and problem responses:

```text
@app\.(get|post|put|patch|delete)|router\.(get|post)|Route\(|@GetMapping|@PostMapping
/openapi|swagger|api/v
create|update|delete|fetch|get[A-Z]|/do[A-Z]
_links|links|hypermedia|HAL|Link:
ETag|If-None-Match|If-Match|Cache-Control|Last-Modified
Allow|OPTIONS
problem\+json|application/problem
```

Build this table and stop. Wait for approval before editing.

| Route | Method | REST level | Drift from `references/rest-rules.md` | Proposed change |
|-------|--------|------------|---------------------------------------|-----------------|

A row with no drift stays as it is. A proposed change names the rule it violates. A rename that breaks a published client stays in the table until the user approves it.

### Fix the approved drift

Edit only the rows the user approved, in this order:

1. Method and status semantics, and one error envelope.
2. API entry point and URI naming.
3. Collection wrappers and pagination where the reference requires them.
4. Representation types separate from persistence models.
5. Hypermedia for client-facing APIs.
6. OpenAPI examples that match the handlers.

Extend the project's error handler, pagination helper, auth middleware, and schema library. Do not add a parallel stack.

A gateway may translate casing or aggregate resources. It must preserve origin status codes.

## Agent instructions in the app

Add or update this section in `AGENTS.md`. Create `CLAUDE.md` containing `@AGENTS.md` only when that file is missing.

```markdown
## API
REST standard: `.agents/skills/audit-restful-api/references/rest-rules.md`
OpenAPI: <path to the spec>
Exceptions:
- <one line each, or "None.">
```

## Verify

Run the repo's API tests and the contract check (`make test`, `make check-api-contract`, or the equivalents you found). Report the commands and their results.

Deliver the audit table, the files and routes changed, the OpenAPI path, and any exceptions.

The audit is unfinished while a finding is neither fixed nor recorded as an exception. That includes an RPC verb path, a `200` response that carries an error body, and an undocumented breaking representation change.
