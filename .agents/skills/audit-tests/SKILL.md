---
name: audit-tests
description: Audits a project's tests against the testing standard, including suites that add friction or do not guard product behaviour. Use when the user asks to check, prune, or assess a test suite.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity via .agents/skills.
metadata:
  version: "1.0.0"
  category: dev
  tags: audit,tests,pytest,vitest
---

# Audit tests

The standard is `references/testing-contract.md`. Read it before judging a test. Audit the project against it. Do not redesign the project. Cite the contract from the project's `AGENTS.md`. Do not paste the rules into a second style guide or tool-specific rule file.

Count first. Read little. One directory at a time.

## Inventory

Do this without opening test files.

Python, when the project uses uv:

```bash
uv run pytest <dir> --collect-only -q | tail -3
uv run pytest <dir> --durations=15 -q
git grep -c "patch(\|MagicMock\|monkeypatch" -- <dir>
wc -l <dir>/test_*.py | sort -n | tail -5
```

Node: `npx vitest run --reporter=verbose`, and the same `git grep` and `wc`. Use the test command named in `AGENTS.md` when it is neither of these.

Classify only the suspicious files (slow, mock-heavy, very large). Read their test names first, bodies only where the name does not settle it.

| Verdict | When |
|---------|------|
| keep | A plausible break in product behaviour fails it, and no other test covers that branch. |
| merge | Copy-pasted cases become one `parametrize`. |
| rewrite | It patches our own code. Replace with a fake at the boundary. |
| delete | It matches a "not worth testing" item, duplicates another test, or fails while the product behaviour is still correct. |

For the few highest-risk tests (auth, money, contracts), break the line the test claims to guard, confirm it fails, and revert at once. Do not do this for the whole suite.

List the standard's "worth testing" items that have no test, such as token verification or money maths. A gap becomes a proposed test in the table. Add it only after approval, and only when it guards product behaviour.

Check the gate: CI runs the project's verify command, with nothing missing and nothing extra. Every marker is registered, and strict markers are on. No CI job collects zero tests. Default `addopts` has no forced coverage and no blanket warning ignores.

Build this table and stop. Wait for approval before editing.

| Path | Verdict | Reason |
|------|---------|--------|

A row's reason names the contract item it follows. A proposed deletion says why the product behaviour stays guarded without that test. Findings that are not test changes (CI, config) go in the report, not into drive-by edits.

## Fix the approved rows

Edit only the rows the user approved.

- Change a test only for its listed verdict. Do not rewrite for style.
- Keep a test whose deletion would reduce the guard on a contract.
- Do not run the full suite more than twice: once before, once after.

## Record the contract

Add or update this line under `## Verify` in `AGENTS.md`. Create `CLAUDE.md` containing `@AGENTS.md` only when that file is missing.

```markdown
Tests: `.agents/skills/audit-tests/references/testing-contract.md`
```

A stack that cannot follow a tier or a runner is one line under `## Exceptions`.

## Verify

Run the project's verify command once after the approved edits (`make check`, or the command `AGENTS.md` names). Report the commands, the test count, and the runtime before and after. Every deletion is listed with its reason.

The audit is unfinished while a finding is neither fixed nor recorded under `## Exceptions` in `AGENTS.md`.
