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
