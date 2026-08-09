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

```bash
powershell -File scripts/Link-Synapse.ps1
```

That creates one junction per skill at `~/.claude/skills/<name>`, plus
`~/.claude/commands/synapse`. Per-skill rather than one junction of `skills/`
because Claude Code discovers personal skills flat — as
`~/.claude/skills/<name>/SKILL.md` — so a single junction would nest everything
a level too deep and nothing would load. Junctions rather than symlinks because
they need no admin rights on Windows.

Re-run the script after adding or removing a skill. `-Remove` unlinks. Real
directories in `~/.claude/skills` are never overwritten, so an unrelated
personal skill sitting there is safe.

Edits are live in every project the moment they're saved — there is no publish
step and no version pinning. That is the deliberate tradeoff: a bad edit is
immediately live everywhere, including mid-session. Work on a branch while a
change is still cooking, and check out `master` when you want the junctions to
serve the known-good state.

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
