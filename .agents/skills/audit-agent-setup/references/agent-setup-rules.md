# Agent setup standard

One source of truth per fact. Short files. A command the agent can run to know whether it is done.

| Id | Rule |
|----|------|
| A1 | `AGENTS.md` exists at the root and is the canonical instruction file. Aim for under 150 lines. |
| A2 | `AGENTS.md` has Commands, Verify, Conventions, and Exceptions sections. Exceptions says `None.` when empty. |
| A3 | `CLAUDE.md` contains only `@AGENTS.md`. |
| A4 | No second copy of the rules in `.cursor/rules`, `GEMINI.md`, `.codex`, or another tool-specific file. |
| A5 | Skills live in `.agents/skills/<id>/SKILL.md`. `.claude/skills` is one symlink to that directory. |
| A6 | Every skill description says what it does and when to use it, in the third person. `SKILL.md` stays under 500 lines. Detail goes in `references/` or `assets/`. |
| A7 | A skill with side effects (commit, push, deploy, delete) is explicit-invoke only: `disable-model-invocation: true` and `agents/openai.yaml` with `allow_implicit_invocation: false`. |
| V1 | One command verifies the whole project (`make check`). `AGENTS.md` tells the agent to run it after every change and before it reports done. |
| V2 | CI runs the same command. The agent and CI cannot disagree. |
| V3 | The command exits non-zero on failure and prints what failed. No interactive prompts. |
| G1 | Commit, push, PR, deploy, and delete happen only when the user asks. |
| G2 | No secrets in the tree. `.env` is ignored and `.env.example` is committed. |
| P1 | Multi-file work starts with a short plan the user can approve. Independent tasks may run in parallel. |
| P2 | Permission allowlists and format-on-save hooks are a per-tool setting. `AGENTS.md` names them. The shared tree holds no tool-specific copy. |

## Evidence

A1 and A2: line count and headings. A3 and A4: file contents and the tree listing. A5 and A7: `jig doctor` and frontmatter. V1 to V3: run the command and read the exit code. V2: the workflow file calls it.
