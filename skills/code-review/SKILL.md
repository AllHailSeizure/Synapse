---
name: code-review
description: >-
  Handle incoming code review feedback with verification before changes. Use
  when review comments land (human or bot) and before implementing suggestions —
  especially if feedback is unclear or technically questionable.
---

# Code Review (receiving)

Technical evaluation, not social performance. Verify before implementing. Ask
before assuming. Correctness over comfort.

## Response pattern

1. **Read** the full feedback without reacting
2. **Understand** — restate the requirement, or ask
3. **Verify** against this codebase
4. **Evaluate** — sound for *this* stack and design?
5. **Respond** — technical ack or reasoned pushback
6. **Implement** — one item at a time; test each

## Forbidden

- Performative agreement ("You're absolutely right!", "Great point!")
- Implementing before verification
- Partial batches when some items are unclear

Clarify unclear items **before** any implementation. Related items break if
you only understood half.

## Source handling

### From the user

Trusted after understanding. Still ask if scope is fuzzy. Skip fluff — act or
give a technical one-liner.

### From external / bot reviewers

Before implementing:

- Correct for this codebase?
- Breaks existing behavior?
- Why does current code look that way?
- Platform/compat constraints?
- Does the reviewer have full context?

Wrong or incomplete → push back with evidence. Can't verify → say what you
need. Conflicts with prior user decisions → ask the user first.

## YAGNI

If "implement it properly" appears: check actual usage. Unused → propose
removal. Used → implement properly.

## Order

1. Clarify unknowns
2. Blocking (breaks, security)
3. Simple fixes
4. Complex fixes
5. Test each; watch for regressions (`verification`)

## Push back when

- Breaks working behavior
- Reviewer lacks context
- Unused feature creep
- Wrong for this stack
- Conflicts with user architecture

How: technical reasoning, specific questions, reference tests/code. No
defensiveness.

## Acknowledge correctly

```
✅ Fixed — [what changed]
✅ Good catch: [issue]. Fixed in [place].
✅ [Just fix and show the diff]

❌ Performative praise / gratitude rituals
```

If you pushed back and were wrong: state the correction factually and fix.
No long apology.

## GitHub threads

Reply in the review comment thread, not as a new top-level PR comment.
