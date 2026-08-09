# Example — SYNAPSE.md for hotel-kline-game

Copy the fenced content below to `SYNAPSE.md` at the root of
`AllHailSeizure/hotel-kline-game`. Everything in it was extracted verbatim from
the three bandaid prompts as they ran before generalization, so behaviour
should be unchanged on the first run.

Kept here as a worked example of a filled-in manifest — the blank template is
`docs/TEMPLATES/SYNAPSE.md`.

---

```markdown
# SYNAPSE.md

Repo configuration for Synapse bandaids. Machine-actionable — keep values
literal. See docs/TEMPLATES/SYNAPSE.md in the Synapse repo for the schema.

## Identity

repo: AllHailSeizure/hotel-kline-game
base: master
stack: Godot 4.6.3-stable, pure GDScript

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
