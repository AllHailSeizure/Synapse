# Synapse Init Implementation Plan

**Goal:** Give any repository a one-command Synapse setup — a deterministic Python scanner that detects everything provable about the repo, and a `/synapse-init` skill that interviews the user about the rest and writes `.synapse/`.

**Architecture:** `apps/synapse_init/scan_project.py` is a self-contained, read-only script that emits one JSON document describing the repo's identity, worktree containers, asset extensions, and candidate verify commands. It never writes and never asks. The `synapse-init` skill runs it by absolute path, asks only about what the scan could not settle, and writes `.synapse/identity.md`, `.synapse/weedeat.md`, and `.synapse/verification.md` from the templates in `docs/TEMPLATES/synapse/`.

**Tech Stack:** Python 3.10+, standard library only (argparse, json, subprocess, pathlib, re), unittest.

## Global Constraints

- The scanner is **read-only**. It writes nothing, creates no directories, and never mutates the target repo.
- The scanner has **no intra-repo imports**. It is invoked by absolute path from any working directory (`python <synapse-root>/apps/synapse_init/scan_project.py --root <repo>`), so it must run without `apps/` on `sys.path`.
- All git access goes through one `git(*args, root)` helper so tests can patch it, mirroring `apps/weedeat/scan.py`.
- Every detected value is reported with its **evidence** (the file or command it came from). A value that cannot be proven is `null`, never a guess.
- `bandaids.md` is **out of scope**. Init writes `identity.md`, `weedeat.md`, and `verification.md` only.
- Init is **additive**. An existing `.synapse/` file is never overwritten and an existing key never changes value; init fills gaps and reports what it left alone.
- Generated files carry **no placeholder text**. A key with no answer is omitted, not written as `<fill this in>`.
- `.synapse/` is committed configuration, so a worktree container inside it (`.synapse/worktrees/`) must be gitignored by that exact path while `.synapse/*.md` stays tracked.
- Python floor is 3.10 (matching `apps/weedeat/pyproject.toml`), so `tomllib` is unavailable — `pyproject.toml` is line-scanned, not parsed.

## JSON contract

The scanner's entire output, produced by `scan(root)` and dumped by `main()`:

```json
{
  "root": "D:/libraries/synapse",
  "identity": {
    "repo": "AllHailSeizure/Synapse",
    "base": "master",
    "stack": [{"name": "python", "evidence": "apps/weedeat/pyproject.toml", "version": ">=3.10"}]
  },
  "worktrees": {
    "containers": [{"path": ".worktrees", "exists": true, "ignored": true, "registered": 3}],
    "foreign_present": [".codex", ".claude"],
    "noise_dir_candidates": [".worktrees/"]
  },
  "assets": {
    "art": [{"ext": ".png", "count": 42}],
    "audio": [],
    "sidecar": [{"ext": ".import", "count": 40, "attaches_to": ".png"}],
    "unclassified": [{"ext": ".bin", "count": 3}],
    "reference_candidates": [{"ext": ".tscn", "count": 12}],
    "resource_prefix": "res://"
  },
  "verify": {
    "candidates": [
      {"label": "full-tests", "command": "python -m unittest discover apps/weedeat/tests",
       "evidence": "apps/weedeat/tests"}
    ]
  },
  "existing_config": {"dir": true, "identity": false, "weedeat": true, "verification": false}
}
```

`label` is one of `focused-tests`, `full-tests`, `build`, `lint`, `typecheck`, `ci`. Every list is sorted deterministically (extensions by descending count then name; candidates by label then command) so two runs on an unchanged repo produce byte-identical output.

---

### Task 1: Scanner skeleton and repo identity

**Files:**
- Create: `apps/synapse_init/__init__.py`
- Create: `apps/synapse_init/scan_project.py`
- Create: `apps/synapse_init/tests/test_scan_project.py`

**Interfaces:**
- Produces: `git(*args, root)`, `detect_identity(root)`, `scan(root)`, `main(argv)`, and the JSON envelope with `identity` populated and the other three sections present but empty.

- [ ] Write failing tests: `parse_repo_slug` maps `git@github.com:Owner/Name.git`, `https://github.com/Owner/Name.git`, and `https://github.com/Owner/Name` all to `Owner/Name`, and returns `None` for a non-GitHub remote; `detect_base` returns `master` from a patched `git symbolic-ref --short refs/remotes/origin/HEAD` of `origin/master`, falls back to `HEAD` when that fails only if it is `master` or `main`, and returns `None` otherwise; `detect_stack` returns `python` with version `>=3.10` for a temp dir holding a `pyproject.toml` containing `requires-python = ">=3.10"`, `godot` for a `project.godot` containing `config/features=PackedStringArray("4.3", "GL Compatibility")` with version `4.3`, and `[]` for an empty dir.
- [ ] Run `python -m unittest apps.synapse_init.tests.test_scan_project -v`; expect `ModuleNotFoundError: No module named 'apps.synapse_init'`.
- [ ] Implement the module docstring, `git()` (a `subprocess.run` wrapper with `capture_output=True, text=True, encoding="utf-8", errors="replace"` returning stripped stdout, empty string on non-zero), `parse_repo_slug`, `detect_base`, `detect_stack` over the marker table (`package.json`→node via `"engines"`/`"node"`, `pyproject.toml`→python via `requires-python`, `setup.py`→python when no `pyproject.toml`, `Cargo.toml`→rust, `go.mod`→go via the leading `go ` line, `project.godot`→godot via the first quoted token of `config/features`, `*.csproj`/`*.sln`→dotnet, `Gemfile`→ruby), `detect_identity`, `scan()` returning the full envelope with empty `worktrees`/`assets`/`verify`, `detect_existing_config`, and `main()` with `--root` (default `.`) and `--indent` (default 2) that exits 1 with `Not a git repository: <root>` on stderr when `git rev-parse --show-toplevel` is empty.
- [ ] Run `python -m unittest apps.synapse_init.tests.test_scan_project -v`; expect pass.
- [ ] Run `python apps/synapse_init/scan_project.py --root .` from the repo root; expect JSON with `"repo": "AllHailSeizure/Synapse"`, `"base": "master"`, and a `python` stack entry.
- [ ] Commit: `feat: add synapse init scanner with repo identity detection`

### Task 2: Worktree container detection

**Files:**
- Modify: `apps/synapse_init/scan_project.py`
- Modify: `apps/synapse_init/tests/test_scan_project.py`

**Interfaces:**
- Consumes: `git()`, `scan()`.
- Produces: `detect_worktrees(root)` filling the `worktrees` section.

- [ ] Write failing tests: with `git` patched to return a two-entry `worktree list --porcelain` blob whose second path is `<root>/.worktrees/topic`, `detect_worktrees` reports a `.worktrees` container with `registered: 1`; a container that exists on disk but holds no registered worktree is still reported with `registered: 0`; `ignored` is `True` only when the patched `check-ignore` returns 0; `foreign_present` lists exactly the marker directories that exist; `noise_dir_candidates` includes every container with a trailing slash plus `.godot/` when `project.godot` exists and not otherwise.
- [ ] Run `python -m unittest apps.synapse_init.tests.test_scan_project -v`; expect `AttributeError` / missing `detect_worktrees`.
- [ ] Implement `detect_worktrees`: parse `git worktree list --porcelain`, treat the first entry as primary, derive each other entry's container as the POSIX-relative parent of its path; union those with `.synapse/worktrees`, `.worktrees`, `worktrees`, `.claude/worktrees`; keep any that is registered or exists on disk; per container record `exists`, `registered`, and `ignored` (`git check-ignore -q <path>` return code 0); list `foreign_present` from `.cursor`, `.codex`, `.vscode`, `.claude`; build `noise_dir_candidates`. Wire it into `scan()`.
- [ ] Run `python -m unittest apps.synapse_init.tests.test_scan_project -v`; expect pass.
- [ ] Run `python apps/synapse_init/scan_project.py --root .`; expect `.worktrees` and `.claude/worktrees` reported with non-zero `registered` counts and `.codex` in `foreign_present`.
- [ ] Commit: `feat: detect worktree containers in the synapse init scan`

### Task 3: Asset extension classification

**Files:**
- Modify: `apps/synapse_init/scan_project.py`
- Modify: `apps/synapse_init/tests/test_scan_project.py`

**Interfaces:**
- Consumes: `git()`, `scan()`.
- Produces: `detect_assets(root)` filling the `assets` section.

- [ ] Write failing tests over a patched `git ls-files -z` blob: given `art/hero.png`, `art/hero.png.import`, `art/tree.png`, `art/tree.png.import`, `scenes/main.tscn`, `src/main.gd`, `.import` is classified as a sidecar with `attaches_to: ".png"` and is absent from `art`; `.png` lands in `art` with `count: 2`; `.tscn` and `.gd` land in `reference_candidates`, not in `art` or `unclassified`; a binary extension outside both tables (a file whose sampled bytes contain `\x00`) lands in `unclassified`; a text extension outside both tables never lands in `unclassified`; `resource_prefix` is `res://` only when `project.godot` exists; entries sort by descending count then extension name.
- [ ] Run `python -m unittest apps.synapse_init.tests.test_scan_project -v`; expect missing `detect_assets`.
- [ ] Implement `detect_assets`: count extensions from `git ls-files -z`; classify in order — sidecar (≥80% of that extension's files still name a tracked path once the trailing `.<ext>` is removed, with `attaches_to` the most common extension among those base paths), then `ART_EXTS` (`.png .jpg .jpeg .gif .webp .bmp .tga .svg .aseprite .ase .pxo .psd .xcf .kra`), then `AUDIO_EXTS` (`.ogg .wav .mp3 .flac .aiff .aup3 .mid`), then `unclassified` when `looks_binary` (a NUL byte in the first 8000 bytes of up to three sampled files) is true, else a text extension. Text extensions with count ≥3 become `reference_candidates`, capped at the top 8, always including `.tscn`, `.tres`, and `.gd` when `project.godot` exists. Wire it into `scan()`.
- [ ] Run `python -m unittest apps.synapse_init.tests.test_scan_project -v`; expect pass.
- [ ] Run `python apps/synapse_init/scan_project.py --root .`; expect `.md` and `.py` in `reference_candidates`, empty `art`/`audio`, and `resource_prefix: null`.
- [ ] Commit: `feat: classify tracked asset extensions in the synapse init scan`

### Task 4: Verify command candidates

**Files:**
- Modify: `apps/synapse_init/scan_project.py`
- Modify: `apps/synapse_init/tests/test_scan_project.py`

**Interfaces:**
- Consumes: `scan()`.
- Produces: `detect_verify(root)` filling the `verify` section.

- [ ] Write failing tests over temp directories: a `package.json` with `{"scripts": {"test": "jest", "build": "vite build", "lint": "eslint ."}}` yields `npm run test` labelled `full-tests`, `npm run build` labelled `build`, and `npm run lint` labelled `lint`, each with evidence `package.json`; malformed JSON yields no candidates and raises nothing; a `pyproject.toml` mentioning `pytest` yields `python -m pytest`; a `tests/` directory holding `test_x.py` with no pytest mention yields `python -m unittest discover tests`; a `Makefile` with a `test:` target yields `make test`; a `.github/workflows/ci.yml` containing `        run: npm ci` yields a `ci`-labelled candidate `npm ci`; candidates are deduplicated by command and sorted by label then command.
- [ ] Run `python -m unittest apps.synapse_init.tests.test_scan_project -v`; expect missing `detect_verify`.
- [ ] Implement `detect_verify` over `package.json` scripts (key match: `test`→full-tests, `test:unit`/`test:watch`→focused-tests, `build`→build, `lint`→lint, `typecheck`/`tsc`→typecheck), `pyproject.toml` text scan (`pytest`→`python -m pytest`, `ruff`→`ruff check .`, `mypy`→`mypy .`), unittest discovery for `tests/` and `apps/*/tests/` directories containing `test_*.py`, `Makefile` targets matching `^(test|build|lint|check|typecheck):`, `Cargo.toml`, `go.mod`, `*.sln`/`*.csproj`, and single-line `run:` values in `.github/workflows/*.yml` capped at 12. Wire it into `scan()`.
- [ ] Run `python -m unittest apps.synapse_init.tests.test_scan_project -v`; expect pass.
- [ ] Run `python apps/synapse_init/scan_project.py --root .`; expect a `full-tests` candidate of `python -m unittest discover apps/weedeat/tests`.
- [ ] Commit: `feat: detect candidate verification commands in the synapse init scan`

### Task 5: The `/synapse-init` skill

**Files:**
- Create: `skills/synapse-init/SKILL.md`
- Create: `commands/synapse-init.md`

**Interfaces:**
- Consumes: the scanner's JSON contract.
- Produces: `.synapse/identity.md`, `.synapse/weedeat.md`, `.synapse/verification.md` in the target repo.

- [ ] Write `skills/synapse-init/SKILL.md` with frontmatter `name: synapse-init` and a description that triggers on setting up, installing, or bootstrapping Synapse in a repository and on `/synapse-init`, and explicitly does not trigger on editing configuration that already exists.
- [ ] Write its body as five steps. **Step 1 — scan:** resolve the scanner as `$CLAUDE_PLUGIN_ROOT/apps/synapse_init/scan_project.py`, falling back to the Synapse checkout path, run `python <path> --root <repo>`, and stop with the scanner's own stderr if it exits non-zero. **Step 2 — read what exists:** read any of the three `.synapse/` files already present and treat every key that already has a value as settled and untouchable. **Step 3 — ask once:** put every open question in a single round — which container holds worktrees (offer the containers the scan found first, `.synapse/worktrees` only when none exists), which `unclassified` extensions are art, audio, sidecar, or none (skip entirely when the list is empty), which candidate is focused tests, full tests, build, and lint (skip a label the scan settled unambiguously), and confirmation of the one-line `stack` string composed from `identity.stack`. **Step 4 — write:** create `.synapse/` if absent and write the three files from `docs/TEMPLATES/synapse/`, filling `identity.md` from `identity`, `weedeat.md`'s `## Assets` from `assets` (`sidecar` extensions also become `## Worktrees` `noise-suffixes`) and `## Worktrees` from the chosen container plus `foreign_present` and `noise_dir_candidates`, and `verification.md` from the confirmed commands; omit every key with no answer, and never emit angle-bracket placeholders. Add the chosen container to `.gitignore` when the scan reported `ignored: false`, as the exact path with a trailing slash. **Step 5 — report:** list the files written, the keys omitted and why, the values left untouched because they already existed, and `git add .synapse .gitignore` as the suggested next command.
- [ ] State the boundaries in the skill: the scanner is read-only, the skill writes only inside `.synapse/` and `.gitignore`, `bandaids.md` is out of scope and is mentioned only if `.github/workflows/` exists, no existing value is overwritten, and no worktree directory is created (`git worktree add` creates it later).
- [ ] Write `commands/synapse-init.md` with a `description` frontmatter line matching the other command files and a body that dispatches to the skill and names the three files it will write.
- [ ] Verify by running the skill against a scratch clone with no `.synapse/` directory: confirm the three files appear, contain no angle brackets (`grep -c "<" .synapse/*.md` returns 0 for each), and that a second run reports every key as already settled and changes nothing (`git diff --exit-code .synapse` succeeds).
- [ ] Commit: `feat: add the synapse-init skill and command`

### Task 6: Honor the configured container in worktree tooling

**Files:**
- Modify: `skills/worktrees/SKILL.md`
- Modify: `apps/weedeat/scan.py`
- Modify: `apps/weedeat/tests/test_scan.py`

**Interfaces:**
- Consumes: `containers:` in `.synapse/weedeat.md`.

- [ ] Write a failing test asserting `DEFAULT_CONTAINERS` includes `.synapse/worktrees` and that `orphan_dirs` finds a stray directory under `.synapse/worktrees` in an unconfigured repo.
- [ ] Run `python -m unittest apps.weedeat.tests.test_scan -v`; expect the new assertions to fail.
- [ ] Add `.synapse/worktrees` to `DEFAULT_CONTAINERS` in `apps/weedeat/scan.py`, ahead of `.claude/worktrees`.
- [ ] Run `python -m unittest apps.weedeat.tests.test_scan -v`; expect pass.
- [ ] Change the directory priority line in `skills/worktrees/SKILL.md` from "explicit user preference → existing `.worktrees/` → existing `worktrees/` → default `.worktrees/`" to "explicit user preference → the first `containers:` entry in `.synapse/weedeat.md` → existing `.worktrees/` → existing `worktrees/` → default `.worktrees/`", and extend the adjacent `git check-ignore` snippet to check the configured container first.
- [ ] Run `python -m unittest discover apps/weedeat/tests -v`; expect the full suite to pass.
- [ ] Commit: `feat: honor the configured worktree container in worktrees and weedeat`

### Task 7: Documentation

**Files:**
- Modify: `README.md`
- Modify: `skills/README.md`
- Modify: `CLAUDE.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: the finished skill and scanner.

- [ ] Add a `## Project setup` section to `README.md` above `## Per-repo configuration and artifacts` documenting `/synapse-init`: what the scanner detects, that it writes nothing, that the skill asks about the rest and writes the three `.synapse/` files, that `bandaids.md` is written by hand from its template, and the direct invocation `python apps/synapse_init/scan_project.py --root <repo>` for inspecting the raw JSON.
- [ ] Add `| `synapse-init` | Detect a repo's setup and write `.synapse/` (`/synapse-init`) |` to the skills table in `skills/README.md`, and a `| `/synapse-init` | `synapse-init` |` row to its Commands table.
- [ ] Add `- `synapse-init` — Scan a repo and write its `.synapse/` configuration (`/synapse-init`)` to the Skills list in `CLAUDE.md` and the matching list in `AGENTS.md`.
- [ ] Verify: `grep -rn "synapse-init" README.md skills/README.md CLAUDE.md AGENTS.md` shows an entry in each, and `grep -rn "synapse_init" README.md` shows the direct invocation path.
- [ ] Commit: `docs: document synapse init`
