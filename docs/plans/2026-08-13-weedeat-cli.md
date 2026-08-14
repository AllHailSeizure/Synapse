# Weedeat Command Interface Implementation Plan

**Goal:** Replace the full-screen Textual reviewer with a line-oriented command interface that uses numeric risk levels, persistent manual tags, and explicit trim commands.

**Architecture:** The scanner owns automatic numeric classification and applies repository-local overrides from `.synapse/weedeat-tags.json`. A standard-library command loop renders branch/worktree rows and delegates confirmed trimming to guarded Git mutation functions; `scan` remains the machine-readable frontend.

**Tech Stack:** Python 3.10+, argparse, JSON, subprocess, unittest

## Global Constraints

- Levels are `0` protected, `1` safe, `2` stale, `3` review, and `4` hold/highest risk.
- `trim N` includes levels `1..N`, requires confirmation, and can never delete level `0`.
- A branch and its attached worktree share one effective tag.
- Primary, configured-protected, locked, and foreign-tool entries are system-protected and cannot be made deletable by a tag.
- Launching `run` never deletes anything without an explicit `trim` command.

---

### Task 1: Numeric classification and persistent tags

**Files:**
- Create: `apps/weedeat/tags.py`
- Modify: `apps/weedeat/scan.py`
- Create: `apps/weedeat/tests/test_tags.py`
- Modify: `apps/weedeat/tests/test_scan.py`

**Interfaces:**
- Produces: `read_tags(root)`, `set_tag(root, kind, target, level)`, `remove_tag(...)`, and survey rows with `level`, `automatic_level`, and association data.

- [x] Write tests for level mapping, system protection, JSON persistence, and branch/worktree tag propagation.
- [x] Run `python -m unittest apps.weedeat.tests.test_tags apps.weedeat.tests.test_scan -v`; expect failures for missing numeric/tag behavior.
- [x] Implement tag persistence and numeric survey rows.
- [x] Run the focused tests; expect pass.

### Task 2: Guarded trim service

**Files:**
- Modify: `apps/weedeat/prune.py`
- Create: `apps/weedeat/trim.py`
- Modify: `apps/weedeat/tests/test_prune.py`
- Create: `apps/weedeat/tests/test_trim.py`

**Interfaces:**
- Consumes: numeric survey rows.
- Produces: candidate planning and confirmed removal for levels `1..N`.

- [x] Write tests proving level `0` is rejected, thresholds select `1..N`, worktrees are removed before associated branches, and failed worktree removal protects its branch.
- [x] Run focused trim/prune tests; expect failures for the missing service.
- [x] Implement minimal guarded pruning and trim orchestration.
- [x] Run focused tests; expect pass.

### Task 3: Line-oriented command loop

**Files:**
- Create: `apps/weedeat/console.py`
- Delete: `apps/weedeat/tui.py`
- Replace: `apps/weedeat/tests/test_tui.py` with `apps/weedeat/tests/test_console.py`

**Interfaces:**
- Consumes: survey, tag, diff, and trim APIs.
- Produces: `review(root, result, input_fn=input, output=stdout)` supporting `list`, `branch ... tag`, `worktree ... tag`, `untag`, `diff`, `trim`, `help`, and `quit`.

- [x] Write command-loop tests for initial rendering, exact tag syntax, untagging, confirmation, invalid commands, and quitting.
- [x] Run console tests; expect failures while `console.py` is absent.
- [x] Implement the standard-library REPL and remove Textual UI code.
- [x] Run console tests; expect pass.

### Task 4: CLI integration and documentation

**Files:**
- Modify: `apps/weedeat/cli.py`
- Modify: `apps/weedeat/pyproject.toml`
- Modify: `apps/weedeat/tests/test_cli_integration.py`
- Modify: `docs/TEMPLATES/synapse/weedeat.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: `console.review` and numeric survey output.
- Produces: non-destructive `weedeat run`, numeric headless output, and updated user guidance.

- [x] Update integration tests to prove `run` does not auto-prune and only opens the command loop on a TTY.
- [x] Implement CLI wiring, remove Textual dependency, and document commands/tag storage.
- [x] Run `python -m unittest discover -s apps/weedeat/tests -v`; expect all tests pass.
- [x] Run `python -m apps.weedeat run --dry-run --no-fetch` and `python -m apps.weedeat scan --no-fetch`; verify the standard entry points.
