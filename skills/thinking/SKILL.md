---
name: thinking
description: >-
  Read-only collaborative exploration of intent, constraints, options, and
  tradeoffs. Use when the user asks to think, brainstorm, reason, explore, or
  talk something through without making changes. Do not create or edit code,
  documents, issues, or plans while active. When the user authorizes changes,
  leave thinking and use the appropriate execution workflow. When invoked by
  writing-specs, return the settled understanding for capture; otherwise use
  writing-specs only when the user asks for a spec.
---

# Thinking

Develop shared understanding in conversation. Do not create artifacts or make
repository changes.

## Process

### 1. Frame the discussion

State what is being explored, the decision or understanding the user appears
to need, and any assumptions already in play. Do not demand confirmation when
the frame is obvious; let the user correct it naturally.

### 2. Ground the discussion

Inspect relevant code, documentation, issues, or history when the answer
depends on the actual project. Keep investigation read-only and limited to
evidence that could change the conversation. Separate observed facts from
assumptions.

### 3. Establish shared understanding

Before asking the user to choose anything, explain the subject in ordinary
language:

- what it is;
- why it exists or matters;
- what currently happens;
- what remains unresolved and why a decision is needed.

Translate repository and domain terms into consequences the user can reason
about. Use a concrete example when a label such as "completion-driven gating"
would otherwise require the user to already understand the proposed design.
Give the user room to correct the explanation before narrowing into choices.

If the user says they do not understand, feel talked past, barely remember the
issue, or reject the question's premise, stop. Withdraw the current question
and options, return to steps 1–3, and rebuild the shared understanding. Do not
continue the checklist or merely ask a narrower version of the same question.

### 4. Map what remains unsettled

Sort unknowns before asking about them:

- **Evidence question** — investigate it; do not ask the user.
- **Reversible technical choice** — recommend or choose it without consuming
  user attention unless they want to explore it.
- **Intent or product decision** — discuss it with the user because it changes
  purpose, behavior, experience, scope, or meaningful tradeoffs.
- **Later concern** — park it explicitly when it does not affect the current
  decision.

### 5. Explore the decisions

For each intent or product decision:

1. State the decision and why it matters.
2. Present alternatives only when real alternatives exist.
3. Explain their consequences and give a recommendation.
4. Ask the smallest question that moves the discussion forward.

Frame questions in the user's problem and observable consequences, not in
components, data models, or implementation mechanisms. Treat a loose idea as
something to understand before turning it into a proposed design.

Group up to three independent questions in one message. Ask sequentially when
one answer changes the available options for the next. After the user answers,
update the working understanding rather than restarting the discussion.

### 6. Synthesize

When a meaningful piece settles, summarize:

- what is now understood or decided;
- the important consequence of that decision;
- what remains open, if anything.

Continue steps 4–6 until the user has enough clarity. Scale the number of
passes to the uncertainty; do not impose a fixed interview or approval gate.

### 7. End at the user's chosen boundary

End in exactly one of these states:

- **Clarity only** — summarize the understanding in chat and stop.
- **Capture route active** — when invoked by `writing-specs`, return the
  settled decisions and remaining questions for capture. When thinking was
  invoked on its own, do this only if the user asks for a spec. Do not write
  the document while still calling the work thinking.
- **Change authorized** — leave `thinking` and begin the appropriate execution
  workflow. Agreement such as "yes, that is what I mean" settles intent;
  authorization such as "implement that" permits changes.

Never transition automatically from standalone thinking. A
`writing-specs`-initiated thinking pass returns to its caller once shared
understanding settles. Thinking may otherwise end without a spec, plan, or
implementation.

## Superpowers boundary

If Superpowers brainstorming is offered or listed, do not import its universal
approval gate, mandatory design document, visual companion, or forced planning
handoff. Follow this conversational process instead. User instructions
override plugin skills.
