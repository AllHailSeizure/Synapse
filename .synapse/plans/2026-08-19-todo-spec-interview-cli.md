# TODO Spec Interview CLI Implementation Plan

**Goal:** Ship a script-only `TODO` CLI that inventories pending specs, interviews the operator, and records approval, plus a spec-writer entrypoint that creates the pending spec and its question file.

**Architecture:** A standalone `apps/todo` Python package owns spec discovery, JSON question validation, terminal rendering, answer collection, and the final filename/title transition. The existing `writing-specs` skill and a new Codex `spec-writer` registration own repository-grounded drafting and emit the JSON contract; the CLI never calls an agent.

**Tech Stack:** Python 3.10+, `argparse`, `json`, `pathlib`, `unittest`/`pytest`, Codex TOML agent registration, Markdown skill documentation.

## Global Constraints

- v1 lists and interviews `SPEC:` rows only.
- Selecting a row always starts its interview.
- Every interview includes the closer, even when the question file is missing or empty.
- Corrupt question files refuse the interview and leave the spec `PENDING`.
- Approval happens only after all questions and the closer complete successfully.
- The CLI makes no model calls and adds no runtime dependency.

## File map

- `apps/todo/domain.py` — discover pending specs, validate question files, append answers, and transition status.
- `apps/todo/console.py` — render inventory/questions and collect answers from a terminal.
- `apps/todo/cli.py` — repository discovery, TTY gate, selection, and process exit codes.
- `apps/todo/__init__.py`, `apps/todo/__main__.py`, `apps/todo/pyproject.toml` — package and `TODO` console entrypoint.
- `apps/todo/tests/` — domain, console, and CLI integration coverage.
- `skills/writing-specs/SKILL.md` — change the drafting handoff to paired `PENDING` spec/questions artifacts and stop-before-approval.
- `.codex/agents/synapse/spec-writer.toml` — bounded Codex drafting agent.
- `AGENTS.md`, `README.md`, `skills/README.md`, `hooks/synapse-briefing.md` — publish the entrypoint and artifact contract.
- `.synapse/specs/2026-08-19 - TODO Spec Interview CLI (IMPLEMENTED).md` — implemented status after all criteria verify.

---

### Task 1: Pending spec inventory and question contract

**Files:**
- Create: `apps/todo/domain.py`
- Create: `apps/todo/tests/test_domain.py`

**Interfaces:**
- Produces: `PendingSpec`, `Question`, `QuestionFileError`, `find_pending_specs(root)`, `load_questions(spec)`.

- [x] Step: write tests for missing inventory, status filtering, sorted labels, missing/empty questions, valid prompts/options/recommendations, and corrupt JSON/schema.
- [x] Step: run `python -m pytest apps/todo/tests/test_domain.py -q` — expect failures because the package does not exist.
- [x] Step: implement the minimal inventory and strict version-1 JSON parser.
- [x] Step: rerun the focused tests — expect pass.

### Task 2: Interview completion and atomic approval

**Files:**
- Modify: `apps/todo/domain.py`
- Create: `apps/todo/console.py`
- Create: `apps/todo/tests/test_console.py`

**Interfaces:**
- Consumes: `PendingSpec`, `Question`.
- Produces: `run_interview(spec, input_fn, output)` and `approve_spec(spec, answers, remarks)`.

- [x] Step: write tests for option/free-text answers, required closer, remarks including `none`, abort without mutation, vanished spec, durable answer section, and synchronized `PENDING` to `APPROVED` rename.
- [x] Step: run `python -m pytest apps/todo/tests/test_console.py -q` — expect failures for missing behavior.
- [x] Step: implement collection in memory and a completion write/rename only after the closer.
- [x] Step: rerun domain and console tests — expect pass.

### Task 3: CLI entrypoint and integration behavior

**Files:**
- Create: `apps/todo/__init__.py`
- Create: `apps/todo/__main__.py`
- Create: `apps/todo/cli.py`
- Create: `apps/todo/pyproject.toml`
- Create: `apps/todo/tests/test_cli.py`

**Interfaces:**
- Consumes: domain inventory and console interview.
- Produces: `TODO` / `python -m apps.todo` interface.

- [x] Step: write tests for git-root discovery, clear empty state, numbered `SPEC:` rows, selection, non-TTY refusal without mutation, corrupt questions, and vanished selection.
- [x] Step: run `python -m pytest apps/todo/tests/test_cli.py -q` — expect failures because the entrypoint is missing.
- [x] Step: implement the minimal `argparse` entrypoint with `--list` for non-interactive inventory.
- [x] Step: run all `apps/todo` tests — expect pass.

### Task 4: Spec-writer entrypoint and workflow documentation

**Files:**
- Modify: `skills/writing-specs/SKILL.md`
- Create: `.codex/agents/synapse/spec-writer.toml`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `skills/README.md`
- Modify: `hooks/synapse-briefing.md`
- Create: `apps/todo/tests/test_spec_writer_contract.py`

**Interfaces:**
- Produces: the documented `*.questions.json` version-1 contract consumed by the CLI.

- [x] Step: write contract tests asserting the skill and agent require `PENDING`, a sibling question file, the closer handoff, and no chat approval/implementation.
- [x] Step: run `python -m pytest apps/todo/tests/test_spec_writer_contract.py -q` — expect failure against current docs/registration.
- [x] Step: update the skill, add the agent, and publish the entrypoint in repository guidance.
- [x] Step: rerun the contract and complete TODO test suites — expect pass.

### Task 5: Verify the approved spec and record completion

**Files:**
- Create: `.synapse/specs/2026-08-19 - TODO Spec Interview CLI (IMPLEMENTED).md`

**Interfaces:**
- Consumes: all implemented behavior and verification evidence.
- Produces: synchronized `IMPLEMENTED` spec record.

- [x] Step: run `python -m pytest apps/todo/tests apps/weedeat/tests -q` — expect all pass.
- [x] Step: install the package editable with `python -m pip install -e apps/todo` and run `TODO --list` in a temporary repository — expect a clear pending inventory/empty state with no model process.
- [x] Step: review every approved-spec success criterion against tests and CLI evidence.
- [x] Step: add the approved spec to the branch as `IMPLEMENTED` with title synchronized only after verification succeeds.
- [x] Step: inspect `git diff --check` and the final branch diff.
