# Synapse

Synapse is a personal skill system for Claude. It installs into any project and enforces structured coding practices through hard directives — mandatory gates with visible outputs, not guidelines to interpret.

## What it is

Synapse is a collection of skills that live in `.claude/skills/synapse/` and are installed into projects via a directory junction (see `synapse-init`). Once installed, Claude reads and follows the skills automatically based on context.

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

Use the `synapse-init` skill. It clones this repo to `~/.claude/synapse` (or pulls if already present) and creates a junction at `.claude/skills/synapse` in the target project. All skills become immediately available.

## Repository structure

```
.claude/
  skills/
    synapse/          # skill files
    synapse-init.md   # install/uninstall skill
CLAUDE.md             # root configuration (also read by Claude)
docs/                 # templates and evolution docs
```
