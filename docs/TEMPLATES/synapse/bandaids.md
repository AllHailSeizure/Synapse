# .synapse/bandaids.md — template

Copy this to `.synapse/bandaids.md` in any repo that runs Synapse bandaids, fill
it in, and commit it. The bandaids read it and `.synapse/identity.md` at Gate 0,
and stop if either is missing.

Only the bandaids read this file. Identity lives in `identity.md` because more
than one tool needs it; the `/weedeat` surveys never load this one.

It is deliberately *not* CLAUDE.md. CLAUDE.md is prose for an agent you're
talking to; this is machine-actionable configuration — commands to run, paths
not to touch, secrets to use. Mixing them makes CLAUDE.md unreadable and makes
this unparseable.

Keep every value literal. An automation reading this cannot ask you what you
meant, so a vague entry becomes either a stop or a wrong guess.

---

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

`Identity` comes from `.synapse/identity.md`; everything else on that list comes
from this file. A bandaid stops the same way whichever file is missing.

`Ignore` is optional everywhere — absent means nothing is filtered. `Secrets`
is required only by the frozen Cursor automations.

There is no fallback to a root `SYNAPSE.md`. If one is still lying around from
the old single-file layout, delete it: leaving it invites a future reader —
human or agent — to treat forgotten standards as current.

## Runner

The Verify and Repro commands run on a GitHub Actions runner, which starts
bare. Anything they invoke — an engine binary, a language toolchain, a linter —
has to be installed by the repo's own workflow before the bandaid job, or every
run stops at the verification gate.
