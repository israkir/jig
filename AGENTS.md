# jig

Conventions and standards for agentic development. Apply them when setting up a new project or checking an existing one. Cursor, Claude Code, ChatGPT Codex, and Antigravity read this file and `.agents/skills/`.

## Where the text lives

Each skill is `.agents/skills/<id>/SKILL.md`. The convention tables are `references/` next to that skill. `assets/` holds templates. Those files are the only copies. Cursor, Claude Code, Codex, and Antigravity all use that directory.

Cursor, Codex, and Antigravity load `.agents/skills/` themselves. Claude Code loads `.claude/skills/`. `jig link <app>` points `.claude/skills` at `.agents/skills` with one symlink, so Claude reads the same tree. `CLAUDE.md` is `@AGENTS.md`. `agents/openai.yaml` inside a skill sets Codex invocation policy.

This repository keeps the skill text in `.agents/skills/` only.

Frontmatter in each `SKILL.md` is the machine-readable catalog (`name`, `description`, `metadata.version`, `metadata.category`, `metadata.tags`). The README table is the human index of the same skills. Do not add a third list.

## Commands

```bash
./bin/jig list
./bin/jig check
./bin/jig show <id>
./bin/jig link <app-repo>
./bin/jig link --user
./bin/jig doctor --user
./bin/jig new <id> --category <category>
./bin/jig eval <id>
python3 -m unittest discover tests
```

Run `./bin/jig check` and the unit tests after every change. CI runs the same two commands.

`link` creates symlinks back to the skill files in this repository. `jig link --user` places the distributed skills in `~/.agents/skills` and points `~/.claude/skills` and `~/.gemini/config/skills` at that directory, so Cursor, Claude Code, Codex, and Antigravity see one tree. `jig link <app>` does the same inside one repository. `metadata.distribute: "false"` stays in this repo (the git skills).

## Changing a convention

Edit the reference file. Keep the procedure in `SKILL.md` as pointers and steps. Bump `metadata.version` when behavior changes. Run `./bin/jig check`.

## Git

Commit and push only when asked. One name per action. The procedure is `.agents/skills/<name>/SKILL.md`. Each agent calls that name.

| Name | Cursor, Claude Code, Antigravity | Codex | ChatGPT |
|------|----------------------------------|-------|---------|
| `commit` | `/commit` | `$commit` | `@commit` |
| `create-branch` | `/create-branch` | `$create-branch` | `@create-branch` |
| `squash` | `/squash` | `$squash` | `@squash` |
| `draft-pr-msg` | `/draft-pr-msg` | `$draft-pr-msg` | `@draft-pr-msg` |

Commit messages follow the `commit` skill, including its rule against trailers.
