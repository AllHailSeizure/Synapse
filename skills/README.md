# Synapse skill suite

Lean, directive skills. Noun-phrase names. Proportional judgment over ceremony.

## Skills

| Skill | Role |
|-------|------|
| `thinking` | Read-only collaborative exploration |
| `writing-specs` | Draft a `PENDING` spec and terminal interview questions |
| `verification` | Claim only what you checked |
| `worktrees` | Isolated workspaces |
| `parallel-agents` | When/how to fan out subagents |
| `writing-plans` | Bite-sized implementation plans |
| `executing-plans` | Inline plan execution + checkpoints |
| `subagent-team-execution` | Fresh subagent per plan task |
| `testing` | TDD default / verification-first when clear |
| `debugging` | Hypotheses → instrument → repro → fix → PR |
| `code-review` | Receiving review feedback rigorously |
| `finishing-branches` | Verify → push → PR |
| `goal-oriented-development` | User-directed issues; no fulfiller |
| `bug-capture` | Sticky-note bug → GitHub issue; no fix |
| `autonomous-work-boundaries` | User intent vs agent execution |
| `bug` | Explicit `/bug` or `$bug` → `bug-capture` |
| `debug` | Explicit `/debug` or `$debug` → `debugging` (Codex; Cursor already has `/debug`) |

`verification` reads repo-specific standard checks, scope mappings, environment
requirements, and completion rules from `.synapse/verification.md` when it is
present. Claims not covered there use the repository's normal documented test,
build, app, or CI path.

`asset-churn-audit` and `worktree-cleanup` (the `/weedeat` skills) moved to
their own plugin: [`weedeat`](https://github.com/AllHailSeizure/weedeat).

## Commands

| Command | Skill | Cursor | Codex | Claude |
|---------|-------|--------|-------|--------|
| `/bug` | `bug-capture` | yes | `$bug` | yes |
| `/debug` | `debugging` | built-in | `$debug` | yes (`commands/debug.md`) |

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
- `writing-specs` captures intent only when explicitly requested; `TODO`
  conducts the later operator interview and records approval
- Neither skill automatically invokes the other
- Keep mechanics, cut ritual
