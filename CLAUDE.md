# Synapse: Root Configuration

This is the root configuration for Synapse—a personal workflow integration system that helps establish and evolve coding standards and practices.

## Philosophy

### Spec-First Development
We work by first establishing *what the code should do*, then building to that spec. User defines behavior and intent; Claude helps clarify, suggests efficient approaches, and watches for unnecessary complexity.

### YAGNI Enforcement
The user recognizes a tendency toward overengineering. Claude actively guards against scope creep, features that aren't justified by the spec, and unnecessary abstractions. Simpler is better.

### Autonomous Integration
Claude works independently within established per-project boundaries, making efficient choices without constant prompts. This frees the user to work on other projects without context-switching burden.

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

1. **You define behavior.** What should the code do? What are the constraints?
2. **Claude helps clarify.** Ask questions, propose approaches, suggest cuts if scope creeps.
3. **Claude implements.** Writes spec-compliant code, runs tests, commits frequently.
4. **You review and direct.** Approve or ask for changes. You're always in control.

---

## Autonomy Model

Claude operates independently within per-project boundaries (see `docs/TEMPLATES/project-claude-template.md`). Generally:

- **Can do autonomously:** Implementation, refactoring for efficiency, running tests, committing with conventional commits, suggesting better approaches
- **Needs approval:** Major architecture changes, new dependencies, schema/database changes, changing testing frameworks
- **Never does:** Introduces features not in spec, overrides user design choices, pushy suggestions about scope

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

Synapse uses focused skills to codify recurring behaviors:

- `over-engineering-guard` — Watch for scope creep, suggest cuts
- `speccing-first` — How to approach spec clarification and intent discovery
- `testing-preferences` — Testing strategy and expectations for this codebase
- `code-review-standards` — How feedback and review work
- `autonomous-work-boundaries` — Decision autonomy and approval points

See `.claude/skills/synapse/` for each skill's full documentation.

---

## Per-Project Setup

Each project gets its own `CLAUDE.md` that inherits from this root and specifies local boundaries. See `docs/TEMPLATES/project-claude-template.md` for the template.

---

**Last updated:** 2026-06-12
