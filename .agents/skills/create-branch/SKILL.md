---
name: create-branch
description: Proposes a git branch and creates it after approval. Use when the user asks to create a branch in the jig repository.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity. Invoked by name.
disable-model-invocation: true
metadata:
  version: "1.1.1"
  category: repo
  tags: git,branch
  distribute: "false"
---

# Create branch

You are helping with **git branching** in **jig** (`.agents/skills/`, `bin/jig`, root docs).

## Goals

1. Choose a **short, kebab-case** branch name that reflects the work (not generic names like `fix` or `update`).
2. Use a **prefix** when it fits: `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`, `test/`, or `ci/`.
3. If the user gave an issue number, include it (e.g. `feat/42-options-positioning-engine`).

## What to do

1. Confirm current branch and working tree status (`git status -sb`). If there are uncommitted changes, say so and ask whether to **stash**, **commit first** (the **`commit`** skill), or **proceed anyway** (creating the branch does not move those changes if they stay in the working tree on the new branch—but switching bases can be risky; be explicit).
2. **Base branch**: default to **`main`** unless the user specifies another branch. If **`main`** does not exist locally, infer the default remote branch (e.g. `git symbolic-ref refs/remotes/origin/HEAD` or `git remote show origin`) or **ask once**.
3. Propose **one** branch name in the form `prefix/summary` (lowercase, hyphens, no spaces).
4. **Approval**: On the first response, prefer **proposal only** (name + commands) unless the user clearly asked you to create the branch now. After they approve (or the name is obvious and they said to run it), run:

   ```bash
   git fetch origin 2>/dev/null || true
   git checkout <base-branch>
   git pull --ff-only  # if upstream/tracking exists; otherwise skip with a note
   git checkout -b <new-branch-name>
   ```

   If **`git pull --ff-only`** fails (diverged history) or there is no tracking branch, stop and explain; do not merge or rebase unless the user asks.

5. Print the **final branch name** and remind them to open a PR against **`<base-branch>`** when ready (e.g. after the **`commit`** skill and the **`draft-pr-msg`** skill → root **`PULL_REQUEST.md`**).

## Edge cases

- If they already have **local commits** on the wrong branch, do **not** rewrite history by default. Offer **`git switch -c <new-branch-name>`** from current HEAD to keep commits, or cherry-pick / reset strategies **only** if they explicitly choose them.
- Remotes other than **`origin`**: use what the repo actually has; say so in the proposal.

## Constraints

- Do **not** force-push or rewrite published history unless the user explicitly asks.
- Do **not** delete branches.
