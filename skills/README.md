# Synapse skill suite

Lean, directive skills. Noun-phrase names. Proportional judgment over ceremony.

## Skills

| Skill | Role |
|-------|------|
| `thinking` | Proportional design-before-build |
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

The two `/weedeat` skills ship a script under `scripts/` and read repo-specific
configuration from `.synapse/weedeat.toml` in the target repo. Schema and
template: [`docs/TEMPLATES/weedeat.toml`](../docs/TEMPLATES/weedeat.toml).

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
| Old brainstorming checklist | 8-step interview, section gates, mandatory specs, visual companion, forced writing-plans — replaced by `thinking` |
| requesting-code-review | Review when useful, not a suite gate |
| writing-skills | Authoring lives with skill-creator, not this runtime suite |
| Goal-fulfiller model | Primary session addresses issues; surveyor + writer only |
| SDD review bureaucracy | No per-task reviewer, 5-round loops, ledgers, or mandatory final branch reviewer |
| TDD Iron Law / delete-and-restart / ask-permission exceptions | Replaced by proportional `testing` |
| Finishing 3-option menu | Always push+PR; merge/discard only on explicit ask |

## Suite-wide rules

- Trivial → just do it
- Ambiguous → 1–3 questions, then act
- Risky / hard to reverse → short design + one yes
- Keep mechanics, cut ritual
