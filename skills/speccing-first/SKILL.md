---
name: speccing-first
description: Two mandatory gates before any implementation in collaborative sessions. Ensures approach is chosen deliberately and behavior is agreed on before any code is written.
---

# Speccing-First

**Scope:** This skill applies to interactive sessions where the user is present. Autonomous agent behavior is governed separately.

## Rule

Do not write any implementation code until both gates below are completed and the user has explicitly signed off on each. This applies regardless of how clear or simple the request seems.

---

## Gate 1: Approach Selection

When the user describes a feature, enumerate the realistic approaches for implementing it before proposing anything.

For each approach, state:
- What it does
- Why it could be the right choice
- Why it might be the wrong choice

Then explicitly rule out approaches that don't fit and explain why. State which approach you recommend and why.

**Do not proceed to Gate 2 until the user has agreed on an approach.**

Example of what this catches: using an LLM to detect specific keywords when deterministic string matching would do the job — a choice that would never have been made if the options had been laid out first.

---

## Gate 2: Behavioral Playback

Before writing any code, state exactly what is about to be built in concrete behavioral terms:

- When X happens, Y occurs
- The user sees / receives Z
- Edge case A is handled by doing B
- This does NOT do C

This is not a description of the architecture or the plan. It is a description of the behavior from the outside. It must be specific enough that if Claude has misunderstood the request, the mismatch is obvious.

**Do not write any code until the user confirms this matches what they had in mind.**

---

## Sign-off

After each gate, ask explicitly:

> "Does this match what you want? Say yes to proceed or tell me what to change."

Do not interpret enthusiasm, silence, or a vague "sounds good" as a yes. Do not carry a gate forward that the user has not confirmed.

---

## If scope expands during implementation

Stop writing code. Treat the new scope as a new request and return to Gate 1.
