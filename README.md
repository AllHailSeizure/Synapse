# Synapse

Synapse is a personal skill system for Claude. It installs into any project and enforces structured coding practices through hard directives — mandatory gates with visible outputs, not guidelines to interpret.

## What it is

Synapse is a Claude Code plugin. Its skills and agents live in `skills/` and `agents/` at the repo root and are installed into any project via Claude Code's native plugin system — no scripts, no symlinks, no junctions. Once installed, Claude reads and follows the skills automatically based on context.

The core principle: every skill defines what Claude must visibly complete before moving to the next step. If a step has no required output, it isn't hard enough.

## Skill inventory

**`over-engineering-guard`** *(collaborative sessions)*
During implementation, classifies anything outside the agreed spec:
- Small implementation decisions → handle in session
- Ambiguous additions → flag and ask
- New features or polish layers → log to GitHub milestone, return to current goal

**`goal-tracking`**
Structures project work as GitHub milestones and issues. One open issue = one active goal. New ideas surface as new issues, not as scope expansion. Reflection gate required before starting the next goal.

**`testing-preferences`**
Testing strategy and expectations. *(pending rewrite)*

**`code-review-standards`**
How feedback and review work. *(pending rewrite)*

**`autonomous-work-boundaries`**
Decision autonomy and approval points for agent sessions. *(pending rewrite)*

**`debugging`**
Hypothesis-driven debugging: cursory look, up to four competing hypotheses,
instrumentation that tells them apart, one repro, then fix and PR. Invoked
directly with `/debug`.

## How the skills chain

`goal-tracking` → ensures the session has a single locked goal with new ideas queued  
`over-engineering-guard` → holds the spec line during implementation, routes exceptions to the milestone  

These three work together in a collaborative session. Autonomous agent behavior is governed by `autonomous-work-boundaries` separately.

## Installing

Synapse is a personal system with one user, so it installs by pointing
`~/.claude/` at this repo rather than by packaging a plugin:

Copy the skills and commands into each agent's config directory:

```bash
powershell -Command "'.claude','.cursor' | % { Copy-Item 'D:\Libraries\Synapse\skills\*' \"$env:USERPROFILE\$_\skills\" -Recurse -Force; Copy-Item 'D:\Libraries\Synapse\commands\*.md' \"$env:USERPROFILE\$_\commands\" -Force }"
```

Every agent discovers personal skills the same way — `<config>/skills/<name>/SKILL.md`
— so one copy command serves all of them.

Re-run it after changing a skill. That's the tradeoff: copies don't go stale on
their own, but they don't update on their own either, so an edit isn't live
anywhere until you re-run. Worth checking when a skill doesn't behave the way
the repo says it should.

Codex is not in that list yet — it installs Synapse as a plugin from the
`codex-release` branch, which is several generations behind. Sorting that out is
its own decision.

## Repository structure

```
skills/
  <skill-name>/SKILL.md    # one directory per skill
commands/
  debug.md                 # slash commands
agents/
  codebase-explorer.md, goal-writer.md, goal-surveyor.md, goal-fulfiller.md
CLAUDE.md                  # root configuration (also read by Claude)
docs/                      # templates and evolution docs
```

Codex CLI support (`.codex/agents/synapse/`) is maintained separately and isn't part of the plugin — Codex's own agent migration system can import directly from this repo's Claude Code layout instead.
