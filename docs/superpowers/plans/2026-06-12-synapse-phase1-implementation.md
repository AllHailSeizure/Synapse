# Synapse Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the foundational structure for Synapse: a root CLAUDE.md, core skills, and per-project templates that enable autonomous, integrated Claude workflows.

**Architecture:** Create a lightweight root CLAUDE.md that establishes philosophy and baseline conventions, then develop five focused skills that codify recurring behaviors. Provide a template for per-project CLAUDE.mds that inherit from root and specify local boundaries. This creates the foundation for iterative discovery and evolution.

**Tech Stack:** Markdown files, YAML frontmatter for skills, git for version control

---

## File Structure

**Files to create:**
- `CLAUDE.md` — Root configuration, philosophy, baseline conventions
- `.claude/skills/synapse/over-engineering-guard.md` — Scope-creep detection and YAGNI enforcement
- `.claude/skills/synapse/speccing-first.md` — How to approach spec/intent clarification
- `.claude/skills/synapse/testing-preferences.md` — Testing philosophy and expectations
- `.claude/skills/synapse/code-review-standards.md` — Code review approach and feedback style
- `.claude/skills/synapse/autonomous-work-boundaries.md` — Decision-making autonomy and approval boundaries
- `docs/TEMPLATES/project-claude-template.md` — Template for per-project CLAUDE.mds
- `docs/EVOLUTION.md` — How the evolution loop works, with checklist for post-project reflection

---

## Tasks

### Task 1: Create Root CLAUDE.md

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Write root CLAUDE.md with philosophy section**

Create `CLAUDE.md` with this content:

```markdown
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
```

- [ ] **Step 2: Commit root CLAUDE.md**

```bash
git add CLAUDE.md
git commit -m "docs: add root CLAUDE.md with philosophy and baseline conventions"
```

---

### Task 2: Create Over-Engineering-Guard Skill

**Files:**
- Create: `.claude/skills/synapse/over-engineering-guard.md`

- [ ] **Step 1: Write the skill file**

Create `.claude/skills/synapse/over-engineering-guard.md`:

```markdown
---
name: synapse:over-engineering-guard
description: Actively identifies and prevents scope creep, unnecessary features, and overengineered solutions. YAGNI enforcement.
type: behavior
applies_to: [all coding projects]
---

# Over-Engineering Guard

The user recognizes a tendency to add unnecessary complexity, abstractions, and features. This skill actively prevents that.

## Principles

- **YAGNI ruthlessly.** If a feature isn't explicitly in the spec, it doesn't exist. No "we might need this later."
- **Simplest thing that works.** Choose the simplest solution that solves the stated problem.
- **Three-line rule.** Don't abstract until you have three instances of the same pattern. One or two similar lines is fine.
- **No hypothetical generalization.** Don't build for cases that don't exist yet.

## When This Skill Activates

When the user describes a feature or asks for implementation:

1. **Listen for scope creep.** "While we're at it, we could also..." is a red flag.
2. **Question necessity.** Is this required by the spec? If not, suggest removing it.
3. **Propose cuts.** If something seems like nice-to-have, say so explicitly.
4. **Be direct.** "This is scope creep. I'd suggest we cut it." Not pushy, but clear.

## Examples

**User:** "We need a user authentication system with email, password reset, two-factor auth, and OAuth integrations."

**Guard response:** "Let me clarify scope. The spec says we need auth, but I don't see email reset, 2FA, or OAuth in the requirements. Are those truly required? Or are we adding them as 'might be useful someday'? I'd suggest we start with the minimum (email + password) and add the rest if you explicitly need it."

**User:** "The test runner should automatically run tests, generate coverage reports, upload to CodeCov, and notify Slack."

**Guard response:** "Scope check: The spec says 'run tests.' I see you wanting coverage reports (reasonable), CodeCov upload (is this needed for Phase 1?), and Slack notifications (nice-to-have?). I'd suggest we do tests + coverage, skip the external uploads for now. What's the real requirement?"

---

## Integration

Use this skill automatically during speccing, planning, and implementation. When you sense scope creep, activate it—make the suggestion explicit and direct.
```

- [ ] **Step 2: Commit the skill**

```bash
git add .claude/skills/synapse/over-engineering-guard.md
git commit -m "skill: add over-engineering-guard for YAGNI enforcement"
```

---

### Task 3: Create Speccing-First Skill

**Files:**
- Create: `.claude/skills/synapse/speccing-first.md`

- [ ] **Step 1: Write the skill file**

Create `.claude/skills/synapse/speccing-first.md`:

```markdown
---
name: synapse:speccing-first
description: Approach to clarifying intent and spec before implementation. Focus on understanding behavior, not building.
type: behavior
applies_to: [all coding projects]
---

# Speccing-First

This skill describes how we approach feature spec and requirements clarification before building.

## Approach

When a user describes a feature or asks to implement something:

1. **Understand behavior, not implementation.** What should this *do*? What's the input, output, constraints?
2. **Ask clarifying questions.** One at a time. Focus on: purpose, success criteria, constraints, edge cases.
3. **Propose approaches.** 2-3 options with trade-offs. Lead with a recommendation.
4. **Get alignment.** Make sure the user agrees on what we're building before we build it.
5. **Write the spec.** Brief but complete—what we're building, constraints, how to know it works.

## Key Principles

- **Spec is a contract.** Once we agree on spec, implementation follows it faithfully. No surprises.
- **Questions before code.** Always clarify before writing implementation.
- **Short spec, not detailed.** A few sentences for simple features, a paragraph or two for complex ones. Just enough to remove ambiguity.
- **Include success criteria.** How do we know this works? What tests pass?

## Example Conversation

**User:** "I need a search function."

**Response:** "Let me clarify. Search for what—documents? Code? In what fields? How exact does the match need to be? Just substring, or fuzzy? Should it be case-sensitive? And what's the output—just a list of results, or with relevance scores?"

**User:** "Search documents by title and content, case-insensitive substring match, returns list of matching documents sorted by relevance."

**Response:** "Got it. One more thing: what determines relevance? Title matches rank higher than content? Or is it based on how many times the term appears?"

**User:** "Title matches rank higher."

**Spec to document:**
```
Search feature:
- Input: search term (string)
- Search: document titles and content (case-insensitive substring match)
- Ranking: matches in titles before matches in content
- Output: list of matching documents, sorted by relevance
- Success: search("react") returns documents with "react" in title or content, titles first
```

Now we build to this spec, no surprises.

---

## Integration

Use this skill whenever spec is unclear. It's collaborative—you're helping the user think through what they actually want, not lecturing them on how to write requirements.
```

- [ ] **Step 2: Commit the skill**

```bash
git add .claude/skills/synapse/speccing-first.md
git commit -m "skill: add speccing-first for clarifying intent before building"
```

---

### Task 4: Create Testing-Preferences Skill

**Files:**
- Create: `.claude/skills/synapse/testing-preferences.md`

- [ ] **Step 1: Write the skill file**

Create `.claude/skills/synapse/testing-preferences.md`:

```markdown
---
name: synapse:testing-preferences
description: Testing philosophy and approach for Synapse projects—when to test, what to test, how to structure tests.
type: behavior
applies_to: [all coding projects]
---

# Testing Preferences

## Philosophy

Tests verify behavior. A test should answer: "Does this code do what it's supposed to do?"

Tests are not:
- Proof of 100% code coverage (coverage is a tool, not a goal)
- Verification of implementation details (test the interface, not the internals)
- Busywork (if a test doesn't provide confidence in behavior, don't write it)

## When to Write Tests

**Critical paths:** Always test the happy path and edge cases for anything users rely on.

**Behavior you're uncertain about:** Use tests to explore the design (TDD-style).

**Refactoring:** Write tests first to lock down behavior, then refactor confidently.

**Bug fixes:** Add a test that reproduces the bug, fix the code, verify test passes.

## Test Structure

One test, one behavior assertion:

```python
def test_search_returns_matching_documents():
    results = search("react")
    assert len(results) > 0
    assert all("react" in doc.title or "react" in doc.content for doc in results)
```

Not:

```python
def test_search():
    # Tests search, parsing, ranking, filtering all at once
    ...
```

## Coverage Goals

Aim for confidence, not a number. Generally:
- **Core logic:** 80%+ coverage
- **Error handling:** Cover the main error paths
- **Edge cases:** If it can break, test it

But 60% coverage of the right code is better than 95% coverage of busywork.

## Test Frameworks

Use what the project already uses. If starting fresh:

**JavaScript/TypeScript:** Jest or Vitest
**Python:** pytest
**Go:** stdlib testing + testify for assertions
**Others:** Language convention

---

## Integration

Before implementing a feature, consider: How will we know it works? Write those tests first, implement to pass them.
```

- [ ] **Step 2: Commit the skill**

```bash
git add .claude/skills/synapse/testing-preferences.md
git commit -m "skill: add testing-preferences for test approach and philosophy"
```

---

### Task 5: Create Code-Review-Standards Skill

**Files:**
- Create: `.claude/skills/synapse/code-review-standards.md`

- [ ] **Step 1: Write the skill file**

Create `.claude/skills/synapse/code-review-standards.md`:

```markdown
---
name: synapse:code-review-standards
description: Code review approach—what to look for, how to give feedback, tone and constructiveness.
type: behavior
applies_to: [all coding projects]
---

# Code Review Standards

## What We Review

**Behavior correctness:** Does the code do what the spec says?

**Efficiency:** Is there a simpler/faster approach?

**Clarity:** Can someone understand this without reading the internals?

**Consistency:** Does it follow the project's patterns?

## What We Don't Nitpick

- Formatting (that's what linters are for)
- Naming that's already clear
- "This could be more functional" when imperative is fine
- Hypothetical future-proofing ("What if we need to scale this?")

## Tone

**Be direct and specific.** Not: "This could be cleaner." Instead: "This function does three things; consider splitting the parsing and validation."

**Suggest, don't demand.** "I'd suggest we move the validation to a separate function" not "You need to refactor this."

**Explain the WHY.** "Caching here could help with performance for large datasets" not just "Add caching."

**Be constructive.** If something seems wrong, ask if there's context you're missing. "I don't see why we need both of these—are they solving different problems?"

## Review Process

When reviewing code:

1. **Run it.** Make sure tests pass, behavior works.
2. **Read for correctness.** Does it match the spec?
3. **Skim for efficiency.** Any obvious improvements?
4. **Check consistency.** Does it follow project patterns?
5. **Provide actionable feedback.** Specific suggestions with rationale.

---

## Integration

Use this skill when reviewing PRs, examining completed features, or suggesting improvements during implementation.
```

- [ ] **Step 2: Commit the skill**

```bash
git add .claude/skills/synapse/code-review-standards.md
git commit -m "skill: add code-review-standards for feedback approach"
```

---

### Task 6: Create Autonomous-Work-Boundaries Skill

**Files:**
- Create: `.claude/skills/synapse/autonomous-work-boundaries.md`

- [ ] **Step 1: Write the skill file**

Create `.claude/skills/synapse/autonomous-work-boundaries.md`:

```markdown
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
```

- [ ] **Step 2: Commit the skill**

```bash
git add .claude/skills/synapse/autonomous-work-boundaries.md
git commit -m "skill: add autonomous-work-boundaries for decision-making guidance"
```

---

### Task 7: Create Per-Project CLAUDE.md Template

**Files:**
- Create: `docs/TEMPLATES/project-claude-template.md`

- [ ] **Step 1: Write the template**

Create `docs/TEMPLATES/project-claude-template.md`:

```markdown
# [Project Name] — CLAUDE.md

**Inherits from:** Root CLAUDE.md in Synapse  
**Project purpose:** [One sentence: what does this project do?]  
**Status:** In development

---

## Overview

[2-3 sentences about the project. What problem does it solve? What's the tech stack? Why are we building this?]

---

## Project-Specific Conventions

[Any conventions specific to this project that differ from root. Examples:
- Testing approach for this project (e.g., "TDD for all features")
- Specific naming conventions ("API endpoints use REST verbs")
- Architecture notes ("Service layer handles business logic; routes are thin")
- Framework/library choices and why
]

---

## Boundaries for This Project

**Claude can work autonomously on:**
- [ ] Writing implementations that match spec
- [ ] Refactoring code for efficiency
- [ ] Running tests and verification
- [ ] Creating commits
- [ ] [Add project-specific autonomy]

**Claude needs approval for:**
- [ ] Adding dependencies
- [ ] Major architecture changes
- [ ] [Add project-specific approval points]

**Claude is blocked from:**
- [ ] [Any areas user handles—e.g., "Deployment to production"]
- [ ] [Add project-specific boundaries]

---

## How This Project Uses Skills

This project uses these Synapse skills:

- `synapse:speccing-first` — How we clarify intent before building
- `synapse:over-engineering-guard` — Watch for scope creep
- `synapse:testing-preferences` — Testing approach
- `synapse:code-review-standards` — How feedback works
- `synapse:autonomous-work-boundaries` — Decision boundaries

[Optional: Note any customizations to these skills for this project]

---

## Key Context

### Architecture

[1-2 paragraphs about how the system works. What are the main pieces? How do they connect?]

### What's In Flight

[Current tasks, branches in progress, decisions being made. Update as work progresses.]

### Known Issues / Constraints

[Anything Claude should know—"We're using an old version of X that has Y limitation" or "This endpoint is slow because Z"]

---

## How We Work on This Project

1. **You describe a feature.** What should it do?
2. **Claude clarifies spec.** Questions, proposed approaches, scope check.
3. **You approve spec.** Or iterate until aligned.
4. **Claude builds.** Spec-compliant implementation with tests.
5. **You review.** Approve or ask for changes.
6. **Claude commits.** Submits changes.

When Claude works without you present (you're on another project):
- Claude operates within the boundaries above
- Makes progress on spec'd work
- Commits frequently
- Awaits approval for anything in the "needs approval" category

---

## Reflection (Post-Project)

After completing milestones, we reflect:
- What patterns worked well?
- What created friction?
- Should anything be codified as a skill or root CLAUDE.md update?

See `docs/EVOLUTION.md` for the reflection checklist.

---

**Last updated:** [Date you created this file]
```

- [ ] **Step 2: Commit the template**

```bash
git add docs/TEMPLATES/project-claude-template.md
git commit -m "docs: add per-project CLAUDE.md template"
```

---

### Task 8: Create Evolution Loop Documentation

**Files:**
- Create: `docs/EVOLUTION.md`

- [ ] **Step 1: Write the evolution guide**

Create `docs/EVOLUTION.md`:

```markdown
# Evolution Loop: How Synapse Grows

Synapse is a living system. Each project is a learning opportunity. This document describes how we identify patterns and evolve the system.

---

## Reflection Checklist

After completing a project or reaching a major milestone, work through this checklist together:

### Patterns That Worked Well

- [ ] **Testing approach:** Did the testing strategy feel right? Should we codify it differently?
- [ ] **Code organization:** Was the project structure clear? Any patterns worth standardizing?
- [ ] **Naming conventions:** Did we converge on naming patterns that felt natural?
- [ ] **Spec process:** Did the speccing-first approach work? Any improvements?
- [ ] **Review process:** Did code review feel constructive and helpful?
- [ ] **Autonomy boundaries:** Were the boundaries clear? Did they feel right?
- [ ] **Tooling:** Did the tools (test framework, linter, etc.) work well?

For each "yes," ask: **Should this be codified into a skill or root CLAUDE.md update?**

### Friction Points

- [ ] **Repeated explanations:** Did we keep re-explaining something? (Candidate for skill or CLAUDE.md)
- [ ] **Unclear decisions:** Were there moments where it was unclear who should decide something? (Review boundaries)
- [ ] **Over-engineering:** Did scope creep happen? How did we catch it? (Refine over-engineering-guard)
- [ ] **Testing gaps:** Were there behaviors we wish we'd tested? (Update testing-preferences)
- [ ] **Review surprises:** Did code review uncover unexpected patterns? (Update code-review-standards)
- [ ] **Context switching:** Was context-switching burden still an issue? (Refine autonomy model)

For each friction point, ask: **What would prevent this next time? Is it a process change, a skill, or documentation?**

### Learnings to Codify

When you identify a pattern or solution:

1. **Write the skill or CLAUDE.md update.** Be specific.
2. **Test it on the next project.** Does it help?
3. **Refine based on feedback.** Skills evolve.
4. **Commit the change.** Keep git history of how Synapse evolved.

---

## Evolution Log

Track major updates to Synapse here:

| Date | Change | Reason |
|------|--------|--------|
| 2026-06-12 | Created Phase 1: root CLAUDE.md, core skills, per-project template | Initial Synapse setup |
| [Date] | [Skill/update] | [Reason from reflection] |

---

## Next Phases (Future)

**Phase 2:** Non-coding projects (game design, hard drive organization, life admin)  
**Phase 3:** MCPs for integrating personal systems (calendar, notes, etc.)  
**Phase 4:** Autonomous task batching (handling multiple projects without context-switching burden)

(These will be designed when Phase 1 is solid and you have more clarity on needs.)

---

**Updated:** 2026-06-12
```

- [ ] **Step 2: Commit the evolution guide**

```bash
git add docs/EVOLUTION.md
git commit -m "docs: add evolution loop guide for post-project reflection"
```

---

### Task 9: Verify Structure with a Setup Checklist

**Files:**
- Create: `docs/GETTING-STARTED.md`

- [ ] **Step 1: Write a quick reference guide**

Create `docs/GETTING-STARTED.md`:

```markdown
# Getting Started with Synapse

## What Is This?

Synapse is a personal workflow system that helps you and Claude work as integrated co-workers on coding projects. It's built on shared understanding, not repeated instructions.

## Current State

**Phase 1 is complete:** You have a root CLAUDE.md, core skills, and templates ready to use.

## Setting Up a New Project

1. **Create the project directory:**
   ```bash
   mkdir ~/path/to/new-project
   cd ~/path/to/new-project
   git init
   ```

2. **Copy the CLAUDE.md template:**
   ```bash
   cp ../Synapse/docs/TEMPLATES/project-claude-template.md CLAUDE.md
   ```

3. **Customize CLAUDE.md for this project:**
   - Add project purpose
   - Specify boundaries (what Claude can/can't do)
   - Add architecture notes
   - Update skills that apply

4. **Create the project structure:**
   ```bash
   mkdir src tests docs
   ```

5. **Commit the initial setup:**
   ```bash
   git add CLAUDE.md
   git commit -m "init: project setup with CLAUDE.md"
   ```

## Working on a Project

1. **Describe the feature:** What should it do?
2. **Claude clarifies spec** (uses `synapse:speccing-first`)
3. **You approve spec**
4. **Claude builds** (writes tests, implements, commits)
5. **You review or Claude continues autonomously**

While you're on another project, Claude works independently within boundaries.

## After a Project

1. **Reflect together** (use checklist in `docs/EVOLUTION.md`)
2. **Identify patterns** to codify
3. **Update root CLAUDE.md or create skills** as needed
4. **Commit changes** so future projects inherit improvements

---

## Key Files

- `CLAUDE.md` (root) — Philosophy, baseline conventions, autonomy model
- `.claude/skills/synapse/` — Core skills (over-engineering guard, speccing-first, etc.)
- `docs/TEMPLATES/` — Template for per-project CLAUDE.mds
- `docs/EVOLUTION.md` — How to reflect and evolve the system
- `docs/superpowers/specs/` — Spec docs for Synapse itself
- `docs/superpowers/plans/` — Implementation plans

---

## Useful Commands

**See all Synapse skills:**
```bash
ls .claude/skills/synapse/
```

**Review root conventions:**
```bash
cat CLAUDE.md
```

**Set up a new project:**
```bash
cp docs/TEMPLATES/project-claude-template.md ~/new-project/CLAUDE.md
```

---

For questions or updates, see `docs/EVOLUTION.md` and `docs/superpowers/specs/2026-06-12-synapse-vision-design.md`.
```

- [ ] **Step 2: Commit the getting-started guide**

```bash
git add docs/GETTING-STARTED.md
git commit -m "docs: add getting-started guide for new projects"
```

---

### Task 10: Final Verification and Structure Check

**Files:**
- No new files, verification only

- [ ] **Step 1: Verify directory structure**

Run:
```bash
cd D:\Libraries\Synapse
find . -type f -name "*.md" -o -name "CLAUDE.md" | sort
```

Expected output should show:
```
./CLAUDE.md
./docs/EVOLUTION.md
./docs/GETTING-STARTED.md
./docs/TEMPLATES/project-claude-template.md
./docs/superpowers/plans/2026-06-12-synapse-phase1-implementation.md
./docs/superpowers/specs/2026-06-12-synapse-vision-design.md
./.claude/skills/synapse/over-engineering-guard.md
./.claude/skills/synapse/speccing-first.md
./.claude/skills/synapse/testing-preferences.md
./.claude/skills/synapse/code-review-standards.md
./.claude/skills/synapse/autonomous-work-boundaries.md
```

- [ ] **Step 2: Verify root CLAUDE.md is readable**

Run:
```bash
head -20 CLAUDE.md
```

Should show the "Synapse: Root Configuration" header and philosophy section.

- [ ] **Step 3: Verify all skills exist**

Run:
```bash
ls .claude/skills/synapse/
```

Should show all five skills:
- `over-engineering-guard.md`
- `speccing-first.md`
- `testing-preferences.md`
- `code-review-standards.md`
- `autonomous-work-boundaries.md`

- [ ] **Step 4: Review git log**

Run:
```bash
git log --oneline
```

Should show all commits from this phase:
- "docs: add getting-started guide..."
- "docs: add evolution loop guide..."
- Various skill commits
- "docs: add root CLAUDE.md..."
- "Initial commit: Synapse vision..."

- [ ] **Step 5: Final commit with summary**

```bash
git add -A
git commit -m "feat: complete Phase 1 implementation

- Root CLAUDE.md with philosophy and baseline conventions
- Five core skills: over-engineering guard, speccing-first, testing, review standards, autonomy
- Per-project CLAUDE.md template
- Evolution loop guide for post-project reflection
- Getting-started guide for new projects

Ready to test with first real project."
```

---

## Spec Coverage Check

**From vision design:**
- ✅ Root CLAUDE.md (philosophy, conventions, autonomy model)
- ✅ Skills for recurring patterns (5 core skills created)
- ✅ Per-project CLAUDE.md template
- ✅ Evolution loop documentation
- ✅ Getting-started guide

**No gaps identified.** Phase 1 is complete and ready for testing with the first real project.

---

## Summary

Phase 1 of Synapse is now complete. You have:

1. **Root CLAUDE.md** — Establishes shared understanding, baseline conventions, autonomy model
2. **Five core skills** — Codify recurring behaviors (YAGNI, speccing, testing, review, autonomy)
3. **Per-project template** — Easy setup for new projects with inherited conventions
4. **Evolution guidance** — How to reflect and grow the system from real experience
5. **Getting-started docs** — Quick reference for setting up and working on projects

The system is ready to be tested with your first real project under Synapse. Follow the checklist in EVOLUTION.md after the first project to identify patterns worth codifying.
