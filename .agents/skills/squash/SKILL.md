---
name: squash
description: Squashes the last N local commits into one after approval. Use when the user asks to squash commits in the jig repository.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity. Invoked by name.
disable-model-invocation: true
metadata:
  version: "1.2.1"
  category: repo
  tags: git,squash
  distribute: "false"
---

# Squash

You are helping **rewrite local git history** in **jig** by squashing the **last _N_ commits** (user-specified integer **N ≥ 2**) into **one** commit with a **single, coherent** message that reflects the combined diff—not a noisy stack of old subjects.

## Goals

1. Take **`N`** from the user’s message (e.g. “squash last 3 commits”). If **`N`** is missing or invalid, **ask once** for a positive integer **`N ≥ 2`**.
2. Produce **one** new commit replacing those **`N`** commits, with:
   - A **Conventional Commits**–style **subject** (`type(scope): imperative summary`, ~72 chars, no trailing period).
   - A **body** that **merges meaningfully**: what changed across the squashed range, **why** if clear from history, and **how to validate** when relevant (`./bin/jig check`).
3. **Do not** invent file-level detail that is not supported by the actual diff or `git log` for the range.

## Preconditions (check before rewriting)

1. Run **`git status -sb`**. If there are **uncommitted** changes, stop and ask: **stash**, **commit first** (the **`commit`** skill), or **abort**—do not squash with a dirty tree unless the user explicitly chooses stash + restore.
2. **Commit count**: ensure **`N`** is **≤** `git rev-list --count HEAD` (or the relevant branch tip). If not enough commits, explain and stop.
3. **Merge commits** in `HEAD~N..HEAD`: if **`git log --oneline --merges -N`** shows merges in that range, **warn** that a plain soft reset may not match intent; offer **abort** or a **manual** `git rebase -i` / different strategy—do not guess complex merge topology.
4. **Already pushed**: if **`git branch -vv`** shows the current branch is **ahead of** `origin/<branch>` by **≥ N** commits that were **already pushed**, squashing **rewrites history**. State clearly that updating the remote will require **`git push --force-with-lease`** (only if the user **explicitly** asks to do that). **Never** force-push without explicit approval.

## Mechanics (default: soft reset)

Preferred flow when the range is **linear** (no merges to preserve):

```bash
# Inspect what will be squashed
git log --oneline -N
git diff --stat HEAD~N..HEAD

# Move branch tip back N commits, keep index + working tree = all changes from those N commits
git reset --soft HEAD~N

# Single commit with merged message (use -m twice or -F; no trailers)
git commit -m "<subject>" -m "<body>"
```

**Do not** use `git commit` **trailer** flags (`--trailer`, `Co-authored-by:`, etc.)—per the **`commit`** skill, omit trailers entirely.

## Merging messages meaningfully

1. Collect **evidence**:
   - **`git log -N --reverse --format=%s`** — subject lines in chronological order.
   - **Optional**: **`git log -N --reverse --format=%b`** — bodies for themes (ignore empty noise).
   - **`git diff --stat HEAD~N..HEAD`** (before reset) or **`git diff --cached --stat`** (after soft reset) — areas touched.
2. **Synthesize** (do **not** concatenate N subjects verbatim):
   - Pick **one** `type` and **scope** that best fits the **combined** change (e.g. `fix(skills)` if the net result is a contract fix).
   - **Subject**: one imperative line describing the **whole** squashed change.
   - **Body**: 3–10 short lines, **wrap ~72 chars**; bullets or short paragraphs listing **logical** changes (dedupe, group by area: e.g. `.agents/skills/`, `bin/jig`, `README.md`).
   - If the **only** net change is trivial (e.g. typo + test), say so briefly.
3. If the user gave a **preferred final subject** or **scope**, prefer that when it matches the diff.

## Approval-first (default)

**Do not** run `git reset` or `git commit` on the first response unless the user **clearly** asked to execute (e.g. “squash last 3 now”, “run it”).

1. First response: show **planned `N`**, **`git log --oneline -N`**, short **diff summary**, **proposed merged subject + body**, and the exact **commands** you would run.
2. After explicit approval, run the squash and show **`git log -1 --format=medium`**.

## Edge cases

- **`N = 1`**: not a squash; explain and stop (or suggest `git commit --amend` if they meant to amend).
- **Detached HEAD** or **rebase in progress**: stop; tell the user to resolve or finish the other operation first.
- **Protected branch** / **shared branch**: warn extra strongly; default to **no** force-push.

## Constraints

- Do **not** force-push or rewrite **remote** history unless the user **explicitly** requests it.
- Do **not** delete branches or run destructive cleanup beyond the requested squash.
- Prefer **`--force-with-lease`** over **`--force`** if a push is explicitly requested after squash.
