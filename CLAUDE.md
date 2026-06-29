# Synapse: Root Configuration

This is the root configuration for Synapse — a personal workflow system that enforces structured coding practices through hard directives, not guidelines.

## Philosophy

Synapse treats Claude as a force multiplier, not a collaborator. Skills are step-by-step directives with mandatory gates and visible outputs — not principles to interpret. Abstract guidance can be rationalized around. A required checklist cannot.

Skills are the authority. When a skill applies, follow it exactly.

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

Every collaborative session follows this structure:

1. **Spec before code.** Run `speccing-first` — approach selection and behavioral playback gates must both pass before any implementation begins.
2. **Goals before session.** If the project has a milestone, surface open issues and confirm which goal is next before starting.
3. **Hold the line.** During implementation, `over-engineering-guard` classifies anything outside the spec. Out-of-scope ideas get logged as GitHub issues, not built.
4. **Reflect between goals.** When a goal closes, explicitly ask whether the next one still makes sense before starting it.

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

Synapse skills are hard directives. Each one defines what Claude must visibly complete before moving to the next step.

- `speccing-first` — Two mandatory gates before any code: agree on the implementation approach, then confirm exact behavior via playback. Collaborative sessions only.
- `over-engineering-guard` — Classifies anything outside the current spec during implementation: handle in session, flag and ask, or log to milestone. Collaborative sessions only.
- `goal-oriented-development` — Structures project work as GitHub milestones and issues. Uses three specialized agents (explorer, goal-writer, goal-fulfiller) to research, write, and execute goals. Replaces `goal-tracking`.
- `testing-preferences` — Testing strategy and expectations for this codebase.
- `code-review-standards` — How feedback and review work.
- `autonomous-work-boundaries` — Decision autonomy and approval points for agent sessions.
- `systematic-debugging` — Structured debugging with a mandatory ruled-out list.

See `.claude/skills/synapse/` for each skill's full documentation.

### Tooling

- `/skill-creator` is an official Anthropic plugin for Claude Code. Use it (via the Skill tool) when creating or refining skills — not `superpowers:writing-skills`.

---

## Per-Project Setup

Each project gets its own `CLAUDE.md` that inherits from this root and specifies local boundaries. See `docs/TEMPLATES/project-claude-template.md` for the template.

Install Synapse skills into a project using the `synapse-init` skill.

---

**Last updated:** 2026-06-28
