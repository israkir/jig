---
name: write-tests
description: Writes a test only when it guards one named break in product behaviour, at the cheapest tier that can catch it. Use when the user asks to add a test, cover new behaviour, or fix a bug.
license: GPL-2.0
compatibility: Cursor, Claude Code, ChatGPT Codex, and Antigravity via .agents/skills.
metadata:
  version: "1.3.0"
  category: dev
  tags: tests,pytest,vitest
---

# Write tests

The standard is `../audit-tests/references/testing-contract.md`. Read it before adding a test. That file is the only copy. Cite it from the project's `AGENTS.md`. Do not paste the rules into a second style guide or tool-specific rule file. To audit, prune, or assess a suite, use the audit-tests skill.

## New behaviour

Write the test first, and only when it guards product behaviour. A test that fails while that behaviour is still correct is friction. Thoroughness, a higher count, or a new function is not a reason to add one.

1. Name the break in a one-line `Guards:` comment: an input and a wrong result. If you cannot name both, do not write the test.
2. Pick the lowest tier in the contract that can catch that break.
3. Take the expected value from the requirement or a worked example.
4. Replace only a process boundary with a hand-written fake or a recorded fixture.
5. Run the test once while the break is still present. The failure is the one the comment names. Then make it pass.

## Bug fix

Write a regression test that fails before the fix and passes after it. The failure is the one the `Guards:` comment names. Do not skip, delete, or weaken a test to get green. `skip`, `xfail`, and `.only` are weakening.

## Refactor, copy, style, docs, config

No new test. Existing tests pass unchanged.

## Record the contract

Add or update this line under `## Verify` in `AGENTS.md`. Create `CLAUDE.md` containing `@AGENTS.md` only when that file is missing.

```markdown
Tests: `.agents/skills/audit-tests/references/testing-contract.md`
```

A stack that cannot follow a tier or a runner is one line under `## Exceptions`.

## Verify

While working, run only the affected file or a selection. Before finishing, run the project's verify command once (`make check`, or the command `AGENTS.md` names). Report the commands and their results.

A test that contradicts a new requirement is rewritten, and the summary names that requirement. When you cannot name one, the production code is what changes.
