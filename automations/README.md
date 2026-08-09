# Bandaid automations

Cursor cloud automations that fire on GitHub events and cut the churn of small,
repetitive work. They run server-side regardless of which editor you're in.

| Bandaid | Fires on | Job |
|---------|----------|-----|
| `bug-bandaid` | issue comment containing `@bug-bandaid` | Patch a small bug: ≤4 hypotheses, one repro, one fix, PR |
| `review-bandaid` | inline PR review comment containing `@review-bandaid` | Evaluate one review thread as a claim: YES / NO / UNVERIFIABLE |
| `merge-bandaid` | PR comment containing `@merge-bandaid` | Resolve a mechanical merge conflict with one merge commit |

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
prompts/*.md            source of truth — generic, reads SYNAPSE.md at Gate 0
Build-Automations.ps1   prompts + repo slug -> importable Cursor JSON
build/<repo>/*.json     generated, gitignored
```

Prompts are markdown, not JSON, because a 20KB prompt stored as one escaped
string is undiffable, and these get edited far more than imported.

## Adding a repo

```bash
powershell -File automations/Build-Automations.ps1 -Repo owner/name -Label "Nice Name"
```

Then import the JSON into Cursor, and commit a `SYNAPSE.md` to the target repo
root — see `docs/TEMPLATES/SYNAPSE.md` for the schema and
`docs/EXAMPLES/SYNAPSE.hotel-kline-game.md` for a filled one.

Without `SYNAPSE.md` every run stops at Gate 0 naming the missing section. That
is deliberate: a bandaid improvising against unknown conventions is the failure
this whole arrangement exists to prevent.

The target repo also needs the secrets named in its manifest available to Cursor
(issue ops and PR ops use separate PATs, scoped per command, never handed to
git).

## Editing a prompt

Edit `prompts/<name>.md`, rebuild, re-import. The frontmatter carries the
trigger type, the mention token, the model, and which manifest sections that
bandaid requires — the body carries everything else and stays repo-agnostic.

If you find yourself wanting to write a repo name, a file path, or a build
command into a prompt, it belongs in that repo's `SYNAPSE.md` instead.
