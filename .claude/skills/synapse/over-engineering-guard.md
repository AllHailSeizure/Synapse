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
