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
