# .synapse/identity.md — template

Copy this to `.synapse/identity.md` in the root of any repo that runs Synapse,
fill it in, and commit it. Every Synapse tool reads this file.

It holds only the facts that more than one tool needs. Anything used by exactly
one tool belongs in that tool's own file — `bandaids.md`, `weedeat.md` — so no
tool ever loads configuration it has no use for.

Keep every value literal. An automation reading this cannot ask you what you
meant, so a vague entry becomes either a stop or a wrong guess.

---

## Identity

```
repo: <owner>/<name>
base: <default branch>
stack: <one line — language, engine, version>
```

`repo` must match the trigger binding, or a bandaid is operating on a repo it
wasn't configured for and will stop. `base` is the default branch name alone —
`master`, not `origin/master`; the asset audit prefixes `origin/` itself when it
resolves a baseline.

---

## Why there is no root SYNAPSE.md

Earlier versions kept all of this in a single `SYNAPSE.md` at the repo root.
Every workstream edited that one file, and an uncommitted edit from one of them
was reset away by another before it was ever committed.

There is deliberately **no fallback** to the old path. A tool that silently
reads a root `SYNAPSE.md` when `.synapse/` is missing would happily serve
whatever stale standards that forgotten file still contains. Missing config
should fail loudly (bandaids) or fall back to documented defaults (the
`/weedeat` surveys) — never to a file nobody remembers writing.
