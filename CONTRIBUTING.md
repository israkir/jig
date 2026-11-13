# Contributing to jig

Thanks for improving these standards. The contract for each one lives under `.agents/skills/`. Every agent reads that directory.

## What belongs here

| In scope | Out of scope |
|----------|----------------|
| A skill directory agents can run from a symlink | A second copy of the same rules for one product |
| CLI changes for discovery and linking | A pasted prompt that restates `references/` |
| `AGENTS.md` when maintainer workflow changes | Secrets or machine-specific paths |

## Add a skill

Run `./bin/jig new <id> --category <category>`. It writes the `SKILL.md` and an `evals/<id>.yaml` from templates. Fill every `TODO`. `<id>` is kebab-case and matches `name`. A skill that checks an existing project against a standard uses the `audit-` prefix. Its `metadata.category` stays the subject, such as `api`.

```yaml
---
name: my-skill-id
description: What it does and when to use it, in the third person. One line, at most 1024 characters.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity via .agents/skills.
metadata:
  version: "1.0.0"
  category: ux
  tags: tag1,tag2
---
```

Put convention tables in `references/`. Put templates in `assets/`. The procedure cites those paths in backticks, for example `` `references/rest-rules.md` ``. `./bin/jig check` verifies the paths exist.

Keep `SKILL.md` as steps: new project versus existing project, then inventory, then edits, then a command to run. Record app-specific exceptions in that repo's `AGENTS.md`. Do not instruct the agent to paste the reference into README or a tool rule.

Set `metadata.distribute: "false"` when the skill applies only to this catalog (see `commit`).

`description` starts with a third-person verb and says "Use when ...". Keep `SKILL.md` under 500 lines. A skill with `disable-model-invocation: true` also needs `agents/openai.yaml`. Every distributed skill has `evals/<id>.yaml`: three prompts that must load it, three that must not, and the first action.

Then:

```bash
./bin/jig check
python3 -m unittest discover tests
./bin/jig eval my-skill-id
```

Add a row to the README standards table.

## Change a skill

1. Edit the reference for a rule change, or `SKILL.md` for a procedure change.
2. Bump `metadata.version` when behavior changes (minor or major). Typos are a patch.
3. Run `./bin/jig check`.

Published `name` values stay stable. The setup skill is `new-project`. The API audit is `audit-restful-api`.

## CLI

`bin/jig` is Python 3, standard library only.

| Command | Purpose |
|---------|---------|
| `list` | Print id, category, and description from frontmatter |
| `check` | Names, descriptions, cited paths, and a single `.agents/skills` tree |
| `show <id>` | Print the procedure |
| `show --full <id>` | Procedure plus references and assets |
| `path <id>` | Print the `SKILL.md` path |
| `compose <id>…` | Print a run order of paths |
| `link <dir>` | Symlink distributed skills into that repo and point `.claude/skills` at them |
| `link --user` | Symlink distributed skills for Cursor, Claude Code, Codex, and Antigravity on this machine |
| `link --dry-run` | Print the plan and write nothing |
| `unlink [--user\|<dir>]` | Remove only links and copies that point into jig |
| `doctor [--user\|<dir>]` | Report missing, broken, or stale links and the fix command |
| `new <id> --category <c>` | Scaffold a skill and its eval file |
| `eval <id>` | Print the skill's trigger prompts and expected first action |
| `list --json` | Catalog as JSON |

Where symlinks are unavailable (Windows without Developer Mode), `link` copies the skill and marks it with `.jig-copy`. `doctor` reports a stale copy; re-run `link` to refresh it.

## Pull requests

- [ ] `./bin/jig check` passes
- [ ] `python3 -m unittest discover tests` passes
- [ ] new skill has an `evals/<id>.yaml`
- [ ] `name` matches the directory
- [ ] version bumped when behavior changed
- [ ] no second copy of a reference in the README or a tool-specific rule
- [ ] no secrets

Commit messages follow the [`commit` skill](.agents/skills/commit/SKILL.md). Branch, squash, and PR drafts are the `create-branch`, `squash`, and `draft-pr-msg` skills. Commit and push only when asked.

```text
feat(skills): add a security-headers standard
fix(api): clarify hypermedia examples in the REST contract
docs: point the README at jig list
```

## License

Contributions are licensed under the same [GPL-2.0](LICENSE) license as the project.
