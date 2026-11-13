---
name: audit-agent-setup
description: Audits how a repository is set up for coding agents against the jig standard, covering AGENTS.md, skill links, the verify command, and duplicate provider files. Use when the user asks to check, tidy, or improve the agent setup of a project.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity via .agents/skills.
metadata:
  version: "1.0.0"
  category: agents
  tags: audit,agents,agents-md,skills,workflow
---

# Audit the agent setup

The standard is `references/agent-setup-rules.md`. Read it before judging anything. Audit the project against it. Do not redesign the project.

## Inventory

Look at the repository root and list what exists:

```text
AGENTS.md  CLAUDE.md  GEMINI.md  .cursor/  .claude/  .codex/  .gemini/  .agents/
Makefile  package.json scripts  pyproject.toml scripts  .github/workflows/
```

Run `<jig>/bin/jig doctor <project>` when jig is installed. It reports missing or broken skill links.

Build this table and stop. Wait for approval before editing.

| Rule | Status | Evidence | Proposed change |
|------|--------|----------|-----------------|

Use the rule ids from the reference. A rule that passes still gets a row, with its evidence. A proposed change names the rule it fixes.

## Fix the approved rows

Edit only the rows the user approved, in the order the reference lists the rules. Prefer deleting a duplicate over adding a file. Do not write a rule into a second place. Keep `AGENTS.md` short: move detail into a skill's `references/` and point to it.

## Verify

Run the project's verify command (`make check` or the equivalent you found) and `jig doctor`. Report the commands and their results.

The audit is unfinished while a failing rule is neither fixed nor recorded under `## Exceptions` in `AGENTS.md`.
