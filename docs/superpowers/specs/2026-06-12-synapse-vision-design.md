# Synapse: Vision & Architecture

**Date:** 2026-06-12  
**Status:** Approved for Phase 1 implementation  
**Scope:** Coding projects (phase 1), expandable to other domains later

---

## Overview

Synapse is a personal workflow integration system designed to create a bidirectional communication channel between the user and Claude. Rather than a static preference database, it's a living system that helps the user discover and codify their own workflow patterns while enabling Claude to work more autonomously and consistently across projects.

The core insight: This isn't about *storing preferences*—it's about *evolving a shared understanding* of how the user works, what matters to them, and how Claude can be a more integrated co-worker.

---

## Problem Statement

The user juggles multiple projects (coding, game design, creative work) simultaneously and struggles with:

1. **Context switching burden** — Constant re-prompting and refocusing slows progress. Instead of switching focus repeatedly, they want Claude to work independently on projects while they're elsewhere.
2. **Preference repetition** — Having to re-explain standards (code style, testing approach, architectural preferences) across projects is friction.
3. **Chaos management** — Natural tendency to work in parallel across multiple things, but no system to keep them coordinated without constant attention.
4. **Overengineering tendency** — They recognize they tend to add unnecessary features and want Claude to actively guard against scope creep.
5. **Workflow discovery** — They don't have a fixed methodology; they actively experiment to find what works. Current setup doesn't support evolving understanding.

---

## Goals

**Primary Goals:**
1. Enable Claude to work autonomously on coding projects without constant context-switching prompts
2. Establish clear, per-project boundaries on what Claude can do independently vs. what needs user input
3. Create a shared understanding of coding conventions, standards, and workflow preferences across projects
4. Build a system that actively evolves from real project experience, not hypothetical preferences
5. Reduce friction through codified patterns while maintaining flexibility for discovery

**Success Criteria:**
- User can start a new coding project and Claude operates within understood conventions without re-explaining them
- Claude can work on one project while user switches contexts without requiring re-prompting
- YAGNI enforcement is explicit and active (Claude watches for overengineering)
- System evolves naturally post-project through structured reflection
- User feels Claude is integrated into their workflow, not a tool they're directing

---

## Phase 1: Coding Projects Foundation

Phase 1 focuses on coding projects because:
- User spends most time here
- Claude's behavior in code is proven and easy to adjust
- Code provides clear, measurable patterns (style, testing, architecture)
- This foundation extends to other domains later

### Core Components

**1. Root CLAUDE.md** (Lightweight, Philosophical)

Establishes the working agreement:
- **Philosophy:** Spec-first approach. User defines what code should *do*; Claude helps clarify intent and suggests efficient approaches. No surprise features.
- **Autonomy model:** Claude makes efficient implementation choices, suggests better alternatives, and actively guards against scope creep (YAGNI focus).
- **Baseline conventions:** Shared coding style, testing philosophy, project organization approach.
- **Evolution process:** System is intentionally living. Post-project reflections surface patterns to codify as skills or CLAUDE.md updates.

**2. Skills** (Focused, Single-Responsibility)

Skills codify recurring patterns and behaviors. Start with core skills, add others as patterns emerge:

- `over-engineering-guard` — Actively identifies scope creep, suggests cuts, enforces YAGNI principle
- `speccing-first` — How Claude helps user nail down intent/behavior before building
- `testing-preferences` — Testing strategy and expectations (TDD vs. verification-first, coverage philosophy, etc.)
- `code-review-standards` — What feedback, tone, and review process look like
- `autonomous-work-boundaries` — How Claude makes decisions independently while respecting user's design choices

Additional skills emerge from project experience (e.g., `refactoring-guards`, `performance-optimization-process`, etc.).

**3. Per-Project CLAUDE.md** (Inheritance + Local Boundaries)

Each project gets a local CLAUDE.md that:
- Inherits baseline conventions from root (no repetition)
- Specifies project-specific boundaries: What can Claude do autonomously? What needs approval?
- References which skills apply to this project
- Documents project-specific context (architecture decisions, key constraints, testing strategy for this project)

Example:
```
# Project: [ProjectName] CLAUDE.md

Inherits from: Root CLAUDE.md
Skills: [speccing-first, testing-preferences, over-engineering-guard]

## Project-Specific Boundaries
- Can: Write implementations, refactor for efficiency, run tests, commit with conventional commits
- Needs approval: Major architecture changes, new dependencies, schema migrations
- Blocked: Introducing features not in spec, changing testing framework

## Project Context
[Architecture overview, key decisions, testing strategy for this specific project]
```

**4. Evolution Loop**

After project completion or major milestone:
- **Reflection:** User and Claude discuss: What patterns worked? What created friction? What surprised us?
- **Pattern identification:** Recurring behaviors that could be codified as skills or CLAUDE.md updates
- **Implementation:** New skills are written, or root CLAUDE.md is updated with discoveries
- **Documentation:** Changes captured so future projects inherit improvements
- System naturally grows from real experience, not speculation. Each project makes the next one easier.

---

## Design Principles

**Modular, Not Monolithic:**
- Root CLAUDE.md stays lightweight and philosophical
- Behavior codified in focused skills, not one giant file
- Easy to update individual skills without touching everything

**Living, Not Static:**
- System is explicitly designed to evolve
- Projects are learning opportunities
- Reflection and feedback loops drive improvements

**Autonomy with Respect:**
- Claude works independently within established boundaries
- User's design choices are never overridden
- Suggestions are offered, but not pushy (especially around scope)

**YAGNI Enforcement:**
- User recognizes tendency to overengineer
- Claude actively guards against scope creep
- Simpler is better; features are justified, not assumed

**Spec-First:**
- User defines behavior; Claude helps clarify and reach understanding
- Implementation follows clear intent, not invention
- Reduces back-and-forth, creates shared understanding

---

## What's Not Included (Phase 1)

- Non-coding projects (game design, tilesets, hard drive organization) — future phases
- Real-time monitoring/autonomous task assignment — start with explicit handoffs
- Automatic context management across dozens of parallel projects — start with manageable project count
- Detailed memory of every conversation — focus on codified patterns in CLAUDE.md + skills

---

## Next Steps

1. Create root CLAUDE.md with baseline philosophy and conventions
2. Develop initial skills (over-engineering-guard, speccing-first, testing-preferences)
3. Establish per-project CLAUDE.md template
4. Run first project through this system, collect feedback
5. Post-project reflection: What worked? What should be codified next?

---

## Success Looks Like

- User starts a new coding project, provides context, and Claude operates within understood conventions
- Claude works autonomously for extended periods without needing re-prompts
- User feels like Claude is a co-worker, not a tool they're directing
- System naturally evolves from project experience
- YAGNI is enforced, scope stays focused
