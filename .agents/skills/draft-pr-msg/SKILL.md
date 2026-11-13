---
name: draft-pr-msg
description: Writes the pull request title and body to PULL_REQUEST.md and does not open the pull request. Use when the user asks to draft that message in the jig repository.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity. Invoked by name.
disable-model-invocation: true
metadata:
  version: "1.3.1"
  category: repo
  tags: git,pull-request
  distribute: "false"
---

# Draft PR message

You are drafting a **pull request title and body** for **jig**, **separate from** creating the branch, committing, or opening the pull request. The primary deliverable is a **new Markdown file** in the repo root; the user can open it and paste into GitHub.

## Inputs

1. Prefer **git context**: `git log main..HEAD --oneline` (or `origin/main..HEAD` if `main` is not local) and `git diff main...HEAD --stat`. If the base branch is not `main`, use the branch the user names.
2. Read **`.github/pull_request_template.md`** when it exists and mirror its sections (e.g. Description, Type of Change, Related Issues, Changes Made, Testing, Code Quality, Documentation, Architecture Compliance, Screenshots/Examples, Checklist, Additional Notes, Reviewer Notes). If the file is missing, use that list as a sensible default structure so the PR body is still complete.

## Output file (required)

1. **Create or overwrite** **`PULL_REQUEST.md`** at the **repository root** (sibling of **`README.md`**).
2. **Structure**:
   - **First line**: `# <Title>` — one line after `# `, imperative mood (e.g. `Add options positioning analytics service`), ≤ ~72 characters of title text, no trailing period.
   - **Blank line**, then the **full PR body** as Markdown (everything that belongs in the GitHub description): mirror the template sections, checkboxes as `[x]` / `[ ]`, accurate **Testing** and **Code Quality** commands for this repo only. This repo has no Makefile. Use **`./bin/jig check`**, **`./bin/jig list`**, **`./bin/jig show <id>`**, and **`python3 -m py_compile bin/jig`** when the CLI changed. Do **not** invent `make` targets.
3. Do **not** wrap the file in an outer fenced code block. The file must be normal Markdown GitHub can read when copied.

## Chat reply (brief)

After writing the file, reply in one short paragraph: confirm the path **`PULL_REQUEST.md`**, repeat the **title** (plain text, no `#`), and note that the **body** is in the file below the title heading. Optionally mention adding **`PULL_REQUEST.md`** to **`.gitignore`** if they want to keep drafts local-only.

## Constraints

- Do **not** create the PR on GitHub unless the user asks.
- Do **not** run destructive git commands.
- End with a one-line reminder to run the **`create-branch`** or **`commit`** skill if they still need those steps.
