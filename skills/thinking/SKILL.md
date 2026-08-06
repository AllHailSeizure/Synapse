---
name: thinking
description: >-
  Proportional design-before-build. Use instead of superpowers brainstorming
  whenever intent is unclear, the change is hard to reverse, touches a shared
  or critical path, or will set a pattern other code will follow. Do not use
  for trivial, obvious, or easily reversed edits — just do those.
---

# Thinking (proportional)

Don't build the wrong thing. Skip interviews, mandatory specs, visual
companions, and forced planning gates.

## Decide in one pass

Ask these risk questions for this decision — not as a label for the whole task:

- Is intent unclear?
- Is this hard to reverse?
- Does it touch a shared or critical path?
- Will it set a pattern other code will copy?

**None of the above → implement.** No questions, no design doc, no menu.

**Ambiguity only →** ask 1–3 focused questions (prefer one message with
options). Then implement. Do not stretch into an interview.

**Real design risk →** write a short design (a few sentences up to a short
outline), get one yes, then implement. Scale to the risk. Skip sections that
don't apply (architecture, data flow, errors, testing).

## Hard bans

- No fixed multi-step interview scripts
- No mandatory design-doc write-up under a specs path
- No "approve each section" gates
- No visual companion offers by default
- No forcing `writing-plans` after every think-through
- No inventing Trivial/Standard/Complex tiers

## If superpowers brainstorming is offered or listed

Ignore its checklist (8-step interview, section-by-section approval, mandatory
design doc, visual companion, forced writing-plans gate). Follow this skill
instead. User instructions override plugin skills.
