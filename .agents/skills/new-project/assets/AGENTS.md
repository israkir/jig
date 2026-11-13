# {{title}}

Surfaces: {{surfaces}}.

## Commands

`make help` lists every target.

| Task | Command |
|------|---------|
| Install | `make install` |
| Verify everything | `make check` |
| Run | See the quick start in `make help` |

## Verify

Run `make check` after every change and before you say the work is done. Report what it printed. A failing check is fixed or reported, never skipped.

## Conventions

- Extend the code that exists. Do not add a parallel stack.
- Read a file before you change it. Keep a change to what was asked.
- Record a decision that the code cannot show under Exceptions.

## Rules

1. Secrets stay out of source. The starter database password is only for the loopback container.
2. Commit and push only when asked.

## Exceptions

None.
