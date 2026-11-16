# Testing standard

This file is the testing standard. A project cites it from `AGENTS.md` and states only its own commands. Where a project file disagrees, fix the one that is wrong.

A test is a tripwire for one specific way an agent could break behaviour that works today. It earns its place only by catching a break in product behaviour. It is not a coverage target. A test that fails while that behaviour is still correct is friction, and it is not added. Thoroughness, a higher count, or a new function is not a reason to write one.

Every new test starts with a one-line `Guards:` comment that names an input and a wrong result (`Guards: a missing amount is stored as zero`). A comment that names neither is not a guard. If you cannot name both, do not write the test.

## Worth testing

Any one of these is enough:

- Money, security, authentication, or data-integrity logic.
- Branching domain logic that can be called as a pure function.
- The failure path of that logic: a missing value, a denied check, a constraint rejection.
- A bug you just fixed (a regression test that fails without the fix).
- A published contract between components: token claims, a message envelope, a schema, a queue.
- A structural invariant that is cheap to check: import boundaries, schema names, a schema hash.

## Not worth testing

- Framework or library behaviour.
- Getters, pass-through functions, and wiring.
- Anything `mypy`, `tsc`, or `eslint` already proves.
- Calls to our own code replaced by a mock, then asserting the mock was called.
- Large snapshots, markup, CSS, and copy.
- A test that re-implements the function it checks, or an expected value copied from the function's current output.
- A second test for a branch another test already covers.
- A test added to be thorough, to raise a count, or because a function is new, when product behaviour would stay guarded without it.

## Tiers

Cheapest first. Run the lowest tier that can catch the break.

| Tier | What | Rule |
|------|------|------|
| T0 static | `ruff`, `mypy`, `tsc`, `eslint` | Always. Near free. |
| T1 offline unit | No network, database, wall clock, or secret | The whole package runs in about 30 s. |
| T2 database | Needs the project's test database | Marker `db`. Run serially. Never mock the database when database behaviour is the point. |
| T3 smoke | One browser path per product | Synthetic data only. At most one. |
| Live | Real provider calls | Marker `live`. Never in the default run. |

## What each change needs

| Change | Test required |
|--------|----------------|
| New behaviour | The lowest tier that can catch the break, written first. T1 unless the break is in the database, the browser, or a provider. |
| Bug fix | A regression test that fails before the fix, for the reason the `Guards:` comment names. |
| Contract change | A contract test in the owning package and a consumer test in the other. |
| Refactor, no behaviour change | None. Existing tests pass unchanged. |
| Copy, style, docs, config | None. |

No row is a quota. A new function with no product behaviour to guard gets no test.

## Fakes, not patches

Replace only what crosses the process boundary: provider HTTP, clock, secret store, LLM. Use a hand-written fake or a recorded fixture. Never patch our own functions to make a test pass.

## Stack conventions

- **Python.** `pytest`, files named `test_<topic>.py`, `parametrize` instead of copy-paste. Register every marker in `pyproject` and run with strict markers. Coverage is off by default and run on demand.
- **Node and TypeScript.** Vitest for pure `lib/` functions. No component or DOM tests unless the component holds logic. Playwright only for the single smoke path.
- **Green.** A project is green when the verify command named in `AGENTS.md` passes. CI runs that same command, plus T2 where it provides a database. A CI job that collects zero tests is a defect.

## How an agent runs tests

1. Run the new test once while the break is still present. The failure is the one the `Guards:` comment names. Then make it pass. The expected value comes from the requirement or a worked example.
2. While working, run only the affected file or a selection. The test passes alone and in any order. A result that can flip without a code change is a defect: leftover rows, a wall clock, a sleep, a random id compared to an exact string.
3. Before finishing, run the project's verify command once.
4. Do not re-run lint or tests after edits that cannot affect them. CI is the full gate.
5. If a test contradicts a new requirement, rewrite it and name that requirement in the summary. Changing an expected value is that kind of change. When you cannot name the requirement, the production code is what changes.
6. Never skip, delete, or weaken a test to get green. A `filterwarnings` ignore, `skip`, `xfail`, and `.only` are weakening.
