# SYNAPSE.md — repo manifest template

Copy this to the root of any repo that runs Synapse bandaids, fill it in, and
commit it. The bandaids read it at Gate 0 and stop if it's missing.

It is deliberately *not* CLAUDE.md. CLAUDE.md is prose for an agent you're
talking to; this is machine-actionable configuration — commands to run, paths
not to touch, secrets to use. Mixing them makes CLAUDE.md unreadable and makes
this unparseable.

Keep every value literal. An automation reading this cannot ask you what you
meant, so a vague entry becomes either a stop or a wrong guess.

---

## Identity

```
repo: <owner>/<name>
base: <default branch>
stack: <one line — language, engine, version>
```

Required by every bandaid. `repo` must match the trigger binding, or the
bandaid is operating on a repo it wasn't configured for and will stop.

## Secrets

```
issues: <ENV_VAR_NAME>
pull-requests: <ENV_VAR_NAME>
```

Cursor-only, and only for the frozen automations under `automations/cursor/`.
The GitHub Actions bandaids authenticate `gh` through the workflow, so a repo
running only those can omit this section entirely.

Names only — never values. Omit a line if that surface isn't used.

## Verify

```
<label>: <exact command>
```

One per line, in the order they should run. Labels are free-form; the
`import` label, if present, runs first. These are the *only* commands a
bandaid runs to validate a change, so anything absent here effectively
doesn't gate a merge.

Example:

```
import: "$GODOT_EXE" --headless --import --path "$WORKTREE"
tests:  "$GODOT_EXE" --headless -s addons/gut/gut_cmdln.gd -gdir=res://Tests -gexit --path "$WORKTREE"
smoke:  pwsh -File Tests/smoke_boot.ps1
lint:   python3 Tools/lint/check_architecture_rules.py
```

## Repro

```
default: <how to deterministically reproduce a reported bug>
fallback: <what to do when the default doesn't fit>
```

Required by bug-bandaid; ignored by the others. This is the highest-leverage
section: a bandaid that can't reproduce a bug stops at Gate 2, so a vague
entry here turns into a stop every time.

Describe a mechanism, not a wish. "Write the request to `user://x.cfg`, run
`addons/y/runner.tscn`" is actionable; "run the game and check" is not.

## Protected

```
read-only: <globs, comma-separated>
no-edit: <descriptions of things that are structurally editable but shouldn't be>
note: <free text for anything the two lines above can't express>
```

Content a bandaid must not modify without explicit per-issue permission.
`read-only` is path-matchable; `no-edit` covers things a glob can't catch
(hand-placed nodes, layout, authored ordering). A conflict or fix touching
anything here is an automatic stop.

Err toward listing too much. A bandaid stopping on protected content costs
you one comment; a bandaid rewriting authored work costs you the work.

## Ignore

```
benign: <output that looks like failure but isn't>
```

Without this, known-harmless noise reads as a failed verification and every
run stops. With it too broad, real failures get swallowed — so name specific
signatures, not whole streams.

## Assets

```
base: <baseline ref, defaults to origin/<Identity base>>
art: <extensions, comma-separated>
audio: <extensions, comma-separated>
sidecar: <generated companion extensions>
references: <globs for files that can reference an asset>
resource-prefix: <how references spell an in-repo asset path>
analyzers: <named format analyzers, comma-separated>
flag: <ext> | <CHURN|REVIEW|KEEP> | <reason>
```

Read by the `asset-churn-audit` skill (`/weedeat`); ignored by the bandaids.
Absent means the audit runs on generic defaults and says so in its own output.

`art`, `audio`, and `sidecar` are the only extensions classified — a repo whose
assets are `.glb` and `.fbx` has to say so. `references` scopes the grep that
proves an asset is used; omit it to search every tracked file, which is slower
and noisier but works anywhere.

`analyzers` opt into format-specific evidence, each encoding one tool's file
format. Without them every verdict rests on reference scanning alone.

| Analyzer | What it settles |
|----------|-----------------|
| `godot-import` | A `.import` diff that only moves `.godot/imported/` cache hashes is machine-local churn; a `uid=` change is not |
| `pixelorama-pxo` | A `.pxo` is a zip — hashing `image_data/*` apart from `data.json` tells a real pixel edit from a bare re-save |

`flag` gives a whole extension a blanket verdict before any other evidence, for
files whose presence in a feature branch is the problem regardless of what
changed inside them. Repeat the line per extension.

Example:

```
base: origin/master
art: .png, .jpg, .jpeg, .aseprite, .pxo
audio: .ogg, .wav, .mp3, .aup3
sidecar: .import, .uid
references: *.tscn, *.tres, *.gd, *.godot
resource-prefix: res://
analyzers: godot-import, pixelorama-pxo
flag: .aup3 | REVIEW | Audacity project (LFS, ~100MB) — a recording session, not a game asset; belongs on an audio branch
```

## Worktrees

```
containers: <dirs this repo creates worktrees under, relative to root>
foreign: <path fragments marking another tool's worktree>
noise-suffixes: <uncommitted suffixes that carry no work>
noise-dirs: <uncommitted path prefixes that carry no work>
protected: <branches never proposed for deletion>
```

Read by the `worktree-cleanup` skill (`/weedeat`); ignored by the bandaids.

The noise lines are the ones that matter. Without them, a repo whose engine
rewrites sidecars on every editor open reports every worktree as holding real
work, and the survey stops meaning anything.

Example:

```
containers: .claude/worktrees, .worktrees
foreign: .cursor, .codex, .vscode
noise-suffixes: .import, .uid
noise-dirs: .godot/, .worktrees/, .claude/worktrees/
protected: master, main
```

---

## Missing sections

A bandaid stops at Gate 0 when a section it requires is absent or empty,
naming the section in its comment. That's intentional: improvising against
unknown conventions is precisely the failure this file prevents.

| Bandaid | Requires |
|---------|----------|
| bug | Identity, Verify, Repro, Protected |
| review | Identity, Verify, Protected |
| merge | Identity, Verify, Protected |
| ci | Identity, Verify, Protected |

`Ignore` is optional everywhere — absent means nothing is filtered. `Secrets`
is required only by the frozen Cursor automations.

`Assets` and `Worktrees` are read only by the `/weedeat` skills, which are
surveys rather than automations: they degrade to generic defaults instead of
stopping, and print a line saying so. No bandaid reads either section.

## Runner

The Verify and Repro commands run on a GitHub Actions runner, which starts
bare. Anything they invoke — an engine binary, a language toolchain, a linter —
has to be installed by the repo's own workflow before the bandaid job, or every
run stops at the verification gate.
