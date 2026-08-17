# Synapse skill suite

Lean, directive skills. Noun-phrase names. Proportional judgment over ceremony.

## Skills

| Skill | Role |
|-------|------|
| `thinking` | Read-only collaborative exploration |
| `writing-specs` | Capture feature intent in a document |
| `verification` | Claim only what you checked |
| `worktrees` | Isolated workspaces |
| `parallel-agents` | When/how to fan out subagents |
| `writing-plans` | Bite-sized implementation plans |
| `executing-plans` | Inline plan execution + checkpoints |
| `subagent-team-execution` | Fresh subagent per plan task |
| `testing` | TDD default / verification-first when clear |
| `debugging` | Hypotheses → instrument → repro → fix → PR (`/debug`) |
| `code-review` | Receiving review feedback rigorously |
| `finishing-branches` | Verify → push → PR |
| `goal-oriented-development` | User-directed issues; no fulfiller |
| `bug-capture` | Sticky-note bug → GitHub issue; no fix |
| `autonomous-work-boundaries` | User intent vs agent execution |
| `asset-churn-audit` | Which assets the branch needs vs churn (`/weedeat`) |
| `worktree-cleanup` | Worktree/branch sprawl, tiered by removal safety (`/weedeat`) |

`verification` reads repo-specific standard checks, scope mappings, environment
requirements, and completion rules from `.synapse/verification.md` when it is
present. Claims not covered there use the repository's normal documented test,
build, app, or CI path.

The two `/weedeat` skills ship a script under `scripts/` and read repo-specific
configuration from the `## Assets` and `## Worktrees` sections of the target
repo's `.synapse/weedeat.md`, plus `.synapse/identity.md` for the baseline
branch. Schema: [`docs/TEMPLATES/synapse/`](../docs/TEMPLATES/synapse/). Unlike
a bandaid, a missing section degrades to generic defaults instead of stopping.

## Commands

| Command | Skill |
|---------|-------|
| `/debug` | `debugging` |
| `/bug` | `bug-capture` |
| `/weedeat` | `asset-churn-audit` + `worktree-cleanup` |

## Dropped / not ported

| Dropped | Why |
|---------|-----|
| `systematic-debugging` | 5 agent types, skeptic gate, escalation cap, cap-out issues — replaced by `debugging` |
| Old brainstorming checklist | 8-step interview, section gates, visual companion, and forced writing-plans — replaced by conversational `thinking` and explicit document capture through `writing-specs` |
| requesting-code-review | Review when useful, not a suite gate |
| writing-skills | Authoring lives with skill-creator, not this runtime suite |
| Goal-fulfiller model | Primary session addresses issues; surveyor + writer only |
| SDD review bureaucracy | No per-task reviewer, 5-round loops, ledgers, or mandatory final branch reviewer |
| TDD Iron Law / delete-and-restart / ask-permission exceptions | Replaced by proportional `testing` |
| Finishing 3-option menu | Always push+PR; merge/discard only on explicit ask |

## Suite-wide rules

- `thinking` is read-only conversation; authorization to change ends it
- `writing-specs` captures intent only when explicitly requested
- Neither skill automatically invokes the other
- Keep mechanics, cut ritual
