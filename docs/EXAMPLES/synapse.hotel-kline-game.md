# Example — `.synapse/` for hotel-kline-game

A worked example of a filled-in manifest set. Copy each fenced block to the
named path under `.synapse/` at the root of `AllHailSeizure/hotel-kline-game`.
The blank templates are in `docs/TEMPLATES/synapse/`.

Most of this was extracted verbatim from the three bandaid prompts as they ran
before generalization, so behaviour should be unchanged on the first run.

Four files, not one, and each tool reads only what it needs: the bandaids read
`identity.md` + `bandaids.md`, interactive verification reads
`verification.md`, and the `/weedeat` surveys read `identity.md` +
`weedeat.md`. None loads another tool's file.

---

## `.synapse/identity.md`

```markdown
# Identity

Shared by every Synapse tool. Machine-actionable — keep values literal.

## Identity

repo: AllHailSeizure/hotel-kline-game
base: master
stack: Godot 4.6.3-stable, pure GDScript
```

## `.synapse/bandaids.md`

```markdown
# Bandaids

Repo configuration for Synapse bandaids. Machine-actionable — keep values
literal. See docs/TEMPLATES/synapse/bandaids.md in the Synapse repo.

## Secrets

issues: GITHUB_ISSUES_PAT
pull-requests: GITHUB_PR_PAT

## Verify

import: "$GODOT_EXE" --headless --import --path "$WORKTREE"
tests:  "$GODOT_EXE" --headless -s addons/gut/gut_cmdln.gd -gdir=res://Tests -gexit --path "$WORKTREE"
smoke:  pwsh -File Tests/smoke_boot.ps1
lint:   python3 Tools/lint/check_architecture_rules.py
lint-self: python3 -m unittest Tests.test_check_architecture_rules

## Repro

default: For story, dialogue, chapter, or choreography bugs, use the storystep
runner. Write the request to `user://story_play_step.cfg` using the existing
StoryPlayStepRequest mechanism, then run from the linked worktree:
`DISPLAY=:1 "$GODOT_EXE" --path "$WORKTREE" addons/story_nodes/play_step_runner.tscn`

fallback: For other bugs, create the smallest possible scratch test scene. At
most one scratch scene and one helper script.

## Protected

read-only: *.png, *.pxo, *.ogg, *.wav, Chapter_*.md
no-edit: hand-placed choreography nodes, tilemap layout, transition-zone direction
note: Animation .tres wiring may be edited. Dialogue JSON is the source of
truth for dialogue and is structurally editable, but its creative text —
wording, story beats, character voice — is protected unless the issue
explicitly supplies the intended change. Never infer dialogue contents from
filenames. Follow every hard gate in CLAUDE.md, including nodes-not-numbers,
dialogue-as-data, reusable-content ownership, comments, inherited scene
ownership, and generic chapter-state access.

## Ignore

benign: Godot shutdown noise involving ObjectDB instances, live resources, or
leaked RIDs.
```

## `.synapse/verification.md`

```markdown
# Verification

Project-specific verification instructions for interactive Synapse work. See
docs/TEMPLATES/synapse/verification.md in the Synapse repo.

## Standard checks

- Focused tests: `"$GODOT_EXE" --headless -s addons/gut/gut_cmdln.gd -gdir=res://Tests -gexit --path "$WORKTREE"`
- Full test suite: `"$GODOT_EXE" --headless -s addons/gut/gut_cmdln.gd -gdir=res://Tests -gexit --path "$WORKTREE"`
- Build/import: `"$GODOT_EXE" --headless --import --path "$WORKTREE"`
- Smoke: `pwsh -File Tests/smoke_boot.ps1`
- Architecture lint: `python3 Tools/lint/check_architecture_rules.py`

## Scope mapping

- GDScript changes: run the focused tests covering the behavior, the full test
  suite, and the build/import check.
- Scene or resource changes: run the build/import check and the smoke check;
  inspect the changed behavior in Godot when the claim is visual or interactive.
- Architecture-rule changes: run the architecture lint and
  `python3 -m unittest Tests.test_check_architecture_rules`.
- Documentation-only changes: inspect the rendered Markdown and verify links;
  no Godot runtime check is required.

## Environment requirements

- Required runtime/version: Godot 4.6.3-stable.
- Required applications: `GODOT_EXE` must resolve to that Godot executable.
- Visual or interactive checks require a display and cannot be claimed from a
  headless-only environment.

## Completion rules

- “Tests pass” requires a zero exit code from the applicable GUT command.
- “Build/import succeeds” requires a zero exit code and no script parse errors.
- “Feature works” requires the applicable automated checks plus direct
  observation when the behavior is visual or interactive.
```

## `.synapse/weedeat.md`

```markdown
# Weedeat

Repo configuration for the /weedeat survey skills. See
docs/TEMPLATES/weedeat.md in the weedeat repo (github.com/AllHailSeizure/weedeat).

## Assets

art: .png, .jpg, .jpeg, .aseprite, .pxo
audio: .ogg, .wav, .mp3, .aup3
sidecar: .import, .uid
references: *.tscn, *.tres, *.gd, *.godot
resource-prefix: res://
analyzers: godot-import, pixelorama-pxo
flag: .aup3 | REVIEW | Audacity project (LFS, ~100MB) — a source recording session, not a game asset; the game never loads one. Belongs in an audio branch unless this PR is specifically about audio production.

## Worktrees

containers: .claude/worktrees, .worktrees, .cursor/worktrees, .codex/worktrees
foreign: .cursor, .codex, .vscode
noise-suffixes: .import, .uid
noise-dirs: .godot/, .worktrees/, .claude/worktrees/, .cursor/worktrees/, .codex/worktrees/
protected: master, main
```

Note there is no `base:` under `## Assets` — it would only repeat `master` from
`identity.md`, which the audit already reads and prefixes with `origin/`.

---

## Notes on the extraction

Two things moved position rather than content:

- `Chapter_*.md` was a stop condition only in merge-bandaid's conflict
  classification. It's listed under `read-only` here, which makes it protected
  for all three — bug-bandaid and review-bandaid previously could have edited
  one. That looks like the intent rather than a deliberate asymmetry, but it is
  a behaviour change worth knowing about.
- The CLAUDE.md hard-gate list was inline in two prompts and referenced
  generically in the third. It now lives in `note`, so all three get it.

`Assets` and `Worktrees` came from two skills that had lived in the game repo's
own `.claude/skills/` with this knowledge hard-coded in their scripts.

## Why separate files instead of one

This started as a single root `SYNAPSE.md`. Every workstream edited that one
file, and while the weedeat sections were being added an uncommitted edit was
reset away by concurrent bandaid work in the same checkout — before it was ever
committed. Separate files give each workstream its own edit surface.

There is deliberately no fallback to the old root path. A tool that quietly read
`SYNAPSE.md` when `.synapse/` was absent would serve whatever stale standards
that forgotten file still held. If a root `SYNAPSE.md` survives in a repo,
delete it.
