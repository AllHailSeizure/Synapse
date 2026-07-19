---
name: goals
description: Goal-oriented development workflow using GitHub milestones and issues. Trigger at the START of every session, when asked "what's next", when you or the user is about to implement something outside the current goal, when starting a new project, or when it's time to write or execute a goal. Use this any time work needs to be oriented, planned, tracked, or executed — even if the user doesn't explicitly say "goals."
---

# Goal-Oriented Development

## Codex Dispatch

Use Codex's `spawn_agent` capability for the named agents in `.codex/agents/synapse/`: `codebase-explorer`, `goal-writer`, `goal-surveyor`, and `goal-fulfiller`. Dispatch them only at the steps named below; the main agent remains responsible for user confirmation and GitHub mutations.

## Purpose

Keep coding focused by maintaining one active goal at a time. Ideas are welcome and should be explored freely. The protection is against *implementation drift* — pivoting to code something new while the current goal is incomplete.

---

## Session Start

At the start of every session, before doing anything else:

1. If the project isn't clear from context, ask: "Which project are we working on?"
2. Load open milestones for that repo — identify the active one (ask if there are multiple)
3. List open issues ordered by priority
4. Surface the next one: "Active goal: [title]. Here's what's involved: [checklist summary]. Ready?"
5. Wait for confirmation before starting

No open milestones → prompt to create one before proceeding.

---

## Exploring Ideas

When a new idea surfaces during a session — yours or the user's:

1. **Explore it.** Ask clarifying questions, discuss pros/cons, get feedback
2. **Don't implement it yet.** Keep exploring conversationally
3. **Only queue it if the user commits.** When they say "let's do this" or "queue this for later," create a formal issue

A conversation like "would a dashboard be useful here?" with back-and-forth discussion is fine and encouraged. The skill only intervenes when someone is about to *start writing code* for something outside the current goal.

---

## Implementation Drift Protection

**Trigger:** You or the user is about to start writing code, creating a new feature, or making a significant architectural change that's not part of the current goal.

When this happens:

1. **Stop.** Don't start writing.
2. **Name it:** "That's not in the current goal. Are we switching?"
3. **Get clarity:** Is this an interruption, or are we intentionally pivoting?
4. **If pivoting:** Confirm the user wants to pause the current goal. Then proceed.
5. **If exploring:** Finish the conversation, then return to the current goal.

The distinction: exploring an idea is fine. Starting to implement it without acknowledging we're leaving the current goal is not.

---

## Writing Goals

When it's time to create a new issue (after the user has committed to it), spawn the **`goal-writer`** subagent with:
- The idea description
- The repo path

The goal-writer researches the codebase and returns a fully-formed, executable issue. Present it to the user for confirmation, then create it in GitHub.

A goal is executable when a future session can begin work without needing to ask setup questions. It must carry:
- **Current state** — what exists now that this goal builds on or changes
- **Done criteria** — specific and verifiable (behavior, tests passing, etc.)
- **Constraints** — stack, patterns to follow, things to avoid
- **Checklist** — concrete ordered steps

---

## Fulfilling Goals

When it's time to execute a goal, spawn the **`goal-fulfiller`** subagent with:
- The full issue content
- The repo path

The goal-fulfiller structures and executes the work, updating the issue checklist as steps complete.

---

## Reflection Gate

When an issue closes:

1. Show what was completed.
2. Show the next issue in the queue.
3. Ask: "Does this still make sense, or has finishing the previous goal changed anything?"

Do not start the next goal until confirmed.

---

## Creating a New Milestone

When starting a new project or feature:

1. Work from goals already described, or if given a high-level direction (e.g. "wrap up level one, finish level two"), spawn **one** `goal-surveyor` subagent with the repo path and the direction. It's the only agent that does a full, project-wide pass — it returns both the shared repo-level survey (tech stack, patterns, conventions, structure) and a candidate list of concrete goals with reasoning. This is the only full codebase survey for the milestone — it does not get repeated per goal, and `goal-writer`/`codebase-explorer` never do this broad a pass on their own.
2. Propose a milestone title and one-sentence description — confirm before creating
3. Spawn goal-writer for each goal to produce executable issues, passing it the shared survey from step 1 as context. This is the point of doing the survey once: with 5 goals or 25, every goal-writer call skips re-deriving tech stack/patterns/conventions and only researches what's specific to its own goal.
4. Present the ordered list to the user — confirm before creating anything
5. Flag uncertain goals; ask whether they belong before including them
