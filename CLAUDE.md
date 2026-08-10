# Synapse: Root Configuration

This is the root configuration for Synapse — a personal workflow system that enforces structured coding practices through hard directives, not guidelines.

## Philosophy

Synapse treats the agent as a force multiplier, not a collaborator. Skills are concrete directives — not vibes — but they stay proportional: trivial work is not put through the same gates as irreversible work. Judgment over ceremony.

Skills are the authority when they apply. Follow them; don't invent extra process.

### Living Evolution
Synapse is intentionally living, not static. Each project is a learning opportunity. Post-project reflection surfaces patterns worth codifying into skills or CLAUDE.md updates.

---

## Baseline Conventions

### Code Style & Naming

**JavaScript/TypeScript:**
- Variable and function names: camelCase
- Class and type names: PascalCase
- Constants: UPPER_SNAKE_CASE
- No unnecessary comments—code should be clear from names and structure
- Prefer explicit over implicit; err toward clarity

**Python:**
- Variable and function names: snake_case
- Class names: PascalCase
- Constants: UPPER_SNAKE_CASE
- Follow PEP 8, but readability over dogma
- Docstrings only when behavior isn't obvious from the name

**General:**
- Avoid over-abstraction; three similar lines is better than a premature abstraction
- Default to no comments; only add when the WHY is non-obvious
- Delete dead code rather than leaving TODO comments

### Testing Philosophy

Tests verify behavior, not implementation. Test the public interface; don't test private details.

- Write tests for critical paths and edge cases
- Prefer verification-first when the behavior is clear; TDD when exploring design
- Test coverage should support confidence in behavior, not hit an arbitrary number
- Each test has one clear assertion (or conceptually related set)

### Project Organization

Each project should have a clear, consistent structure:

```
project/
├── CLAUDE.md (local, inherits from root)
├── src/ (implementation)
├── tests/ (tests, mirror src structure)
├── docs/ (project-specific docs)
└── README.md (what this project is)
```

### Commits

Conventional Commits format:

```
feat: description
fix: description
refactor: description
test: description
docs: description
```

Short subject line, blank line, optional body with detail.

---

## How We Work Together

1. **User-directed issues.** Surface open issues when useful; the user picks what to address. Do not auto-select "next."
2. **Reflect between issues.** When an issue closes, ask whether another still makes sense before starting it.

### Memory Scope

Before saving anything to memory, ask: should this apply to this project only, or everywhere? Project-specific context goes in memory files. Universal behavioral instructions go in CLAUDE.md. That's a design decision — don't make it unilaterally.

---

## Autonomy Model

Claude operates independently within per-project boundaries (see `docs/TEMPLATES/project-claude-template.md`). Generally:

- **Can do autonomously:** Implementation, refactoring for efficiency, running tests, committing with conventional commits, suggesting better approaches
- **Needs approval:** Major architecture changes, new dependencies, schema/database changes, changing testing frameworks
- **Never does:** Introduces features not in spec, overrides user design choices, acts on new ideas without logging them first

---

## Evolution Loop

After completing a project or reaching a major milestone:

1. **Reflect together.** What patterns worked? What created friction?
2. **Identify patterns.** Are certain behaviors worth codifying as skills?
3. **Codify.** New skills are written, or root CLAUDE.md updated
4. **Document.** Changes committed so future projects inherit improvements

See `docs/EVOLUTION.md` for detailed reflection checklist.

---

## Skills

Synapse skills are hard directives. Judgment over ceremony — no fixed interview gates for trivial work.

- `thinking` — Proportional design-before-build (replaces ceremony brainstorming)
- `verification` — Claim only what you checked; proportional; no substitute harnesses
- `testing` — TDD when exploring; verification-first when behavior is clear
- `goal-oriented-development` — User-directed issues (intent + evidence); no goal-fulfiller
- `debugging` — Hypotheses fast, instrument, one repro, fix, PR (`/debug`)
- `bug-capture` — Sticky-note capture (`/bug`); record for later, don't fix
- `autonomous-work-boundaries` — What the agent owns vs what needs Nate
- `writing-plans` / `executing-plans` — Plan when the work needs it; execute without endless loops
- `worktrees` / `parallel-agents` / `subagent-team-execution` — Isolation and delegation
- `code-review` — Receive feedback rigorously; no performative agreement
- `finishing-branches` — Verify → push → PR; merge stays user-initiated

See `skills/` and `skills/README.md`.

### Tooling

- `/skill-creator` for authoring/editing skills — not a runtime skill in this suite.

---

## Per-Project Setup

Each project gets its own `CLAUDE.md` that inherits from this root and specifies local boundaries. See `docs/TEMPLATES/project-claude-template.md` for the template.

Synapse installs by copying `skills/` and `commands/` into each agent's config directory — see README. No plugin, no marketplace, no publish step. Re-run the copy after changing a skill.

---

**Last updated:** 2026-08-06
