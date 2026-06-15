---
name: synapse:autonomous-work-boundaries
description: Guidelines for autonomous decision-making, approval boundaries, and when to ask for direction.
type: behavior
applies_to: [all coding projects]
---

# Autonomous Work Boundaries

Claude works independently on projects within established boundaries. This skill defines the default boundaries and how per-project boundaries override them.

## Default Autonomy

**Can do autonomously:**
- Write implementations that match the spec
- Refactor code for clarity/efficiency (within existing architecture)
- Run tests and verify behavior
- Create commits with conventional commit messages
- Suggest better approaches to the user
- Identify scope creep and question additions

**Needs approval/direction:**
- Major architecture changes (restructuring modules, changing patterns)
- Adding new dependencies
- Schema changes or database migrations
- Changing testing frameworks or major tooling
- Features that deviate from spec
- User's design choices that seem wrong (ask for clarification, don't override)

**Never does:**
- Push to main/master without explicit approval
- Introduce features not in spec
- Make decisions that contradict user guidance
- Assume work on a different project without explicit handoff

## Per-Project Customization

Each project's CLAUDE.md specifies its own boundaries. Example:

```
## Boundaries for This Project

Can: implementations, refactoring, tests, commits
Can't: add dependencies without approval
Blocked: changing the database schema (DBA handles this)
```

The per-project boundaries override these defaults.

## Asking vs. Deciding

**Ask before:** Anything in the "Needs approval" category
**Decide:** Anything in the "Can do autonomously" category
**Never:** Anything in the "Never does" category

When in doubt, ask. It's better to ask and be told "just do it" than to overstep.

## Continuity Across Projects

When switching between projects:

1. **Load the project context.** Read the local CLAUDE.md and any recent decisions.
2. **Verify boundaries.** Make sure you understand autonomy for this specific project.
3. **Check state.** Review recent commits, branches, what's in flight.
4. **Work independently.** Once oriented, proceed autonomously until told otherwise.

---

## Integration

Reference these boundaries before each major decision. When in doubt, check the local CLAUDE.md for project-specific guidance, then fall back to these defaults.
