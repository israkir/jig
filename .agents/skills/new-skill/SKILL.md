---
name: new-skill
description: Scaffolds a new skill in the jig repository from the template and its eval file. Use when the user asks to add a skill to jig.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity. Invoked by name.
metadata:
  version: "1.0.0"
  category: repo
  tags: skills,scaffold
  distribute: "false"
---

# New skill

Run `./bin/jig new <id> --category <category>`. It writes `.agents/skills/<id>/SKILL.md` from `assets/SKILL.md` and `evals/<id>.yaml` from `assets/eval.yaml`.

Then:

1. Replace every `TODO` in both files. Keep the description to what the skill does and when to use it.
2. Put convention tables in `references/` and cite them in backticks from `SKILL.md`.
3. Add a row to the README standards table.
4. Run `./bin/jig check` and `python3 -m unittest discover tests`.

Report the commands you ran and their results.
