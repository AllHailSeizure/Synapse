---
description: Survey what's overgrown in this repo — asset churn in the branch, worktree and branch sprawl — and report; never delete
---

# /weedeat

Clear the weeds: things that accumulated on their own and nobody planted. Two
skills cover the two kinds, and both are read-only surveys that end in a report
plus commands for the user to run.

| Argument | Skill |
|---|---|
| `assets`, `churn`, `branch`, `diff`, `pr` | `asset-churn-audit` |
| `worktrees`, `branches`, `sprawl`, `repo` | `worktree-cleanup` |
| none | both, asset churn first |

Pick from the user's words when the argument doesn't match the table — "is this
PR too big" is the asset audit, "what can I delete" is the cleanup. When it's
genuinely ambiguous, run both; they don't interfere.

Follow the invoked skill as the source of truth. Both read repo-specific
configuration from `.synapse/weedeat.toml`; if that file is missing, say so once
in the report rather than silently running blunt, and offer to write one from
`docs/TEMPLATES/weedeat.toml`.

## The boundary

**Report, then stop.** Neither skill deletes, reverts, or stages anything, and
neither do you under this command. Present the findings and the exact commands,
and wait.

If the user then authorizes a tier — "drop the churn", "remove the safe ones" —
that authorizes exactly that tier for that run. It is not authorization for
REVIEW or HOLD, and it does not carry to the next invocation.

When both skills run, report them as two sections under one summary. Lead with
the counts and the single most important risk in each, not a wall of paths.
