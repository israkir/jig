<div align="center">

<h1>&#128221; jig</h1>

<p>
  <strong>Conventions and standards for agentic development</strong>
</p>

<p>
  <a href="https://github.com/israkir/jig/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-GPL--2.0-22c55e?style=flat-square" alt="License: GPL-2.0"/>
  </a>
  <img src="https://img.shields.io/badge/Cursor-Ready-7c3aed?style=flat-square&logo=cursor&logoColor=white" alt="Cursor Ready"/>
  <img src="https://img.shields.io/badge/Claude_Code-Compatible-7c3aed?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code Compatible"/>
  <img src="https://img.shields.io/badge/ChatGPT-Codex-10a37f?style=flat-square" alt="ChatGPT Codex"/>
  <img src="https://img.shields.io/badge/Antigravity-Ready-1a73e8?style=flat-square" alt="Antigravity Ready"/>
  <img src="https://img.shields.io/badge/PRs-Welcome-ec4899?style=flat-square" alt="PRs Welcome"/>
</p>

<p>
  <a href="#why">Why</a>
  &middot;
  <a href="#use">Use</a>
  &middot;
  <a href="#standards">Standards</a>
  &middot;
  <a href="#stack">Stack</a>
  &middot;
  <a href="#contributing">Contributing</a>
  &middot;
  <a href="#license">License</a>
</p>

</div>

---

<a name="why"></a>

### Why

jig is the standard a coding agent follows when it starts a project or checks one that already exists. The rules live here once. [Cursor](https://cursor.com), [Claude Code](https://claude.ai/code), ChatGPT Codex, and [Antigravity](https://antigravity.google) read that same copy.

A new project is scaffolded to the standard. An existing project is compared with it, and only the drift is changed.

---

<a name="use"></a>

### &#128640; Use

Clone jig once. Link it once. Then any agent, in any folder, can start a project or check one.

```bash
# macOS / Linux
git clone https://github.com/israkir/jig.git ~/git/jig
~/git/jig/bin/jig link --user
```

```powershell
# Windows (PowerShell)
git clone https://github.com/israkir/jig.git "$env:USERPROFILE\git\jig"
python "$env:USERPROFILE\git\jig\bin\jig" link --user
```

The same words work in Cursor, Claude Code, Codex, and Antigravity.

| You want | Say this |
|----------|----------|
| Start a project | `Use the new-project skill. The project name is Northwind. I need an API and a database.` |
| Check a project | `Use the audit-restful-api skill. Audit this project.` |

Run `~/git/jig/bin/jig doctor --user` any time to confirm every agent sees the skills. It names the broken link and the command that fixes it. `jig link --dry-run` previews a link and `jig unlink` removes only what jig made.

`new-project` creates the project and links it to jig. A skill whose name starts with `audit-` compares the project with a standard and waits before it edits. `jig list` prints the skills.

To carry the skills inside one repository, for the people who clone it:

```bash
~/git/jig/bin/jig link /path/to/app
```

---

<a name="standards"></a>

### &#127760; Standards

Setup, then API.

<table>
  <thead>
    <tr>
      <th>Step</th>
      <th>Standard</th>
      <th>What it sets</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><a href="./.agents/skills/new-project/SKILL.md"><code>new-project</code></a></td>
      <td>A minimal API, web app, and database, alone or together. <a href="./.agents/skills/new-project/references/layout.md">Layout</a>.</td>
    </tr>
    <tr>
      <td>2</td>
      <td><a href="./.agents/skills/audit-restful-api/SKILL.md"><code>audit-restful-api</code></a></td>
      <td>An existing API is audited against the REST standard. <a href="./.agents/skills/audit-restful-api/references/rest-rules.md">Standard</a>.</td>
    </tr>
    <tr>
      <td>3</td>
      <td><a href="./.agents/skills/audit-agent-setup/SKILL.md"><code>audit-agent-setup</code></a></td>
      <td>A project's own agent setup is audited: one <code>AGENTS.md</code>, one skills tree, one verify command. <a href="./.agents/skills/audit-agent-setup/references/agent-setup-rules.md">Standard</a>.</td>
    </tr>
  </tbody>
</table>

Each standard is a skill: a short procedure plus a contract in `references/`. The app records local facts and exceptions in its own `AGENTS.md` and cites the contract. It does not keep a second copy.

`./bin/jig list` prints the live catalog.

---

<a name="stack"></a>

### &#9881; Stack

`bin/jig` needs Python 3.

`new-project` scaffolds one stack. Use it when the new project matches. A different language, framework, or database is an exception recorded in that project's `AGENTS.md`.

| Piece | Requirement |
|-------|-------------|
| Tasks | GNU Make |
| API | Python 3.12 or newer, and uv |
| Web | Node.js 20.9 or newer, and the npm shipped with it |
| Database | Docker or Podman. Postgres 18 runs in a container on `127.0.0.1` |

Library floors are the newest set that install together. A package manager may select a newer release above a floor. The files are [`apps/api/pyproject.toml`](./.agents/skills/new-project/assets/api/pyproject.toml) and [`apps/web/package.json`](./.agents/skills/new-project/assets/web/package.json).

| Surface | Libraries |
|---------|-----------|
| API | FastAPI 0.162.4, Pydantic 2.14.3, uvicorn 0.54.0 |
| API dev | httpx2 2.16.0, mypy 2.4.1, pytest 9.2.0, Ruff 0.17.4 |
| Database | Alembic 1.20.1, psycopg 3.3.8, SQLAlchemy 2.1.8 |
| Web | Next.js 16.4.5, React 19.1.0, TypeScript 5.8.3, ESLint 9.26.0, Vitest 3.1.2, Prettier 3.5.3 |

---

<a name="contributing"></a>

### &#129309; Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

1. Run `./bin/jig new <id> --category <category>`. Put the rules in `references/` and cite them.
2. Add a row to the table above.
3. Run `./bin/jig check` and `python3 -m unittest discover tests`.

---

<a name="license"></a>

### &#128196; License

GPL-2.0 &copy; [israkir](https://github.com/israkir)

---

<div align="center">
  One standard, read by every coding agent
</div>
