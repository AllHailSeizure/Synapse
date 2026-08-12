# Bandaid automations

Automations that fire on GitHub events and cut the churn of small, repetitive
work. They run server-side regardless of which editor you're in.

| Bandaid | Fires on | Job |
|---------|----------|-----|
| `bug-bandaid` | issue comment containing `@bug-bandaid` | Patch a small bug: ≤4 hypotheses, one repro, one fix, PR |
| `review-bandaid` | inline PR review comment containing `@review-bandaid` | Evaluate one review thread as a claim: YES / NO / UNVERIFIABLE |
| `merge-bandaid` | PR comment containing `@merge-bandaid` | Resolve a mechanical merge conflict with one merge commit |
| `ci-bandaid` | PR comment containing `@ci-bandaid` | Fix one failing CI check: one repro, one causal fix, one commit |

## What a bandaid is for

Small, annoying, menial work — the kind that stacks up because you're busy with
the real problems. A bandaid is a **patch**, not an investigation. Its budgets
(≤12 investigative ops, ≤3 files, ≤100 lines) aren't safety limits, they're the
definition of the job: anything that doesn't fit was never patch-shaped.

So a STOP is a classification, not a failure. It means *this is real work* — and
because a successful bandaid opens a PR that closes the issue, whatever stays
open is exactly what needs you. The sieve does the triage; absence is the
signal. That's also why a bandaid never touches priority labels: priority is
severity, and difficulty is a different axis.

For the interactive counterpart — a real bug, where you're present and want to
explore — use the `debugging` skill (`/debug`). Same epistemics, opposite
posture on boundaries: `debugging` generates a fresh hypothesis set and keeps
going, because you're there to steer.

## Layout

```
claude/skills/<name>/SKILL.md   source of truth — generic, reads .synapse/ at Gate 0
claude/stub.yml                 the per-repo workflow stub
cursor/                         frozen — the retired Cursor implementation
```

The skills ship in the Synapse plugin. The real workflow logic lives in
`.github/workflows/bandaids.yml` at the repo root, called as a reusable
workflow, so an edit there lands in every repo at once.

## Adding a repo

1. Copy `claude/stub.yml` to the target repo's `.github/workflows/bandaids.yml`.
   It's identical in every repo — nothing to fill in.
2. Add a `CLAUDE_CODE_OAUTH_TOKEN` secret to the repo (or the account). Generate
   it with `claude setup-token`; runs bill against the subscription.
3. Commit `.synapse/identity.md` and `.synapse/bandaids.md` to the target repo
   — see `docs/TEMPLATES/synapse/` for the schema and
   `docs/EXAMPLES/SYNAPSE.hotel-kline-game.md` for a filled one.

Without those files every run stops at Gate 0 naming the missing section. That
is deliberate: a bandaid improvising against unknown conventions is the failure
this whole arrangement exists to prevent.

The runner starts bare, so whatever the repo's Verify and Repro commands invoke
must be installed by the workflow before the bandaid job — see the Runner
section of the template.

## Editing a prompt

Edit `claude/skills/<name>/SKILL.md` and push. Target repos pick it up on the
next fire; there is no build, import, or copy step.

If you find yourself wanting to write a repo name, a file path, or a build
command into a prompt, it belongs in that repo's `.synapse/bandaids.md` instead.

## Cursor

`cursor/` holds the retired implementation: three prompts and the PowerShell
builder that turned them into importable Cursor JSON. It is frozen — disable the
automations in Cursor's UI and don't edit these. They exist so the arrangement
can be restored if the Actions version doesn't hold up.
