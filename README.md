# Synapse

Synapse is a personal skill system for Claude. It installs into any project and enforces structured coding practices through hard directives — mandatory gates with visible outputs, not guidelines to interpret.

## What it is

Synapse is a Claude Code plugin. Its skills and agents live in `skills/` and `agents/` at the repo root and are installed into any project via Claude Code's native plugin system — no scripts, no symlinks, no junctions. Once installed, Claude reads and follows the skills automatically based on context.

The core principle: every skill defines what Claude must visibly complete before moving to the next step. If a step has no required output, it isn't hard enough.

## Skill inventory

**`speccing-first`** *(collaborative sessions)*
Two mandatory gates before any code is written:
1. Enumerate implementation approaches, rule out wrong ones, agree on method
2. State exact behavior in concrete terms ("when X, Y happens") and get confirmation

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

**`systematic-debugging`**
Structured debugging with a mandatory ruled-out list. *(pending rewrite / new)*

## How the skills chain

`speccing-first` → ensures approach and behavior are agreed before implementation begins  
`goal-tracking` → ensures the session has a single locked goal with new ideas queued  
`over-engineering-guard` → holds the spec line during implementation, routes exceptions to the milestone  

These three work together in a collaborative session. Autonomous agent behavior is governed by `autonomous-work-boundaries` separately.

## Installing into a project

Add the marketplace once, then install the plugin:

```
/plugin marketplace add AllHailSeizure/synapse#claude-release
/plugin install synapse@synapse
```

`main` is the working branch — skills get changed and tested here first. `release` only moves forward once a change has been tried in a real project; that's the deliberate publish step, and it's what the marketplace pointer above tracks. `/plugin marketplace update` picks up whatever is currently on `release` — nothing changes for an installed project until that branch moves.

To update: `/plugin marketplace update synapse`. To disable: `/plugin disable synapse@synapse`. To remove: `/plugin uninstall synapse@synapse`.

## Repository structure

```
.claude-plugin/
  plugin.json       # plugin manifest
  marketplace.json  # self-hosted marketplace listing this plugin
skills/
  speccing-first/SKILL.md
  testing-preferences/SKILL.md
  goal-oriented-development/SKILL.md
agents/
  codebase-explorer.md, goal-writer.md, goal-surveyor.md, goal-fulfiller.md
CLAUDE.md           # root configuration (also read by Claude)
docs/                # templates and evolution docs
```

Codex CLI support (`.codex/agents/synapse/`) is maintained separately and isn't part of the plugin — Codex's own agent migration system can import directly from this repo's Claude Code layout instead.
