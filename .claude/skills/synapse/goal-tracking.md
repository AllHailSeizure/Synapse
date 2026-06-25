---
name: synapse:goal-tracking
description: Structures project work into GitHub milestones and issues. Use when starting a new project or feature to organize goals, track progress, and queue new ideas without derailing current work.
type: behavior
applies_to: [all projects with GitHub repositories]
---

# Goal Tracking

## Purpose

Prevent task drift by maintaining a single source of truth for project goals in GitHub. The current goal is always a single open issue. New ideas become new issues — they are never acted on in the current session.

## Structure

- **Milestone** = the project or feature being built
- **Issues** = individual goals within that milestone
- **Issue checklist** = the concrete steps to complete that goal
- **New ideas** = new issues added to the milestone, not touched until the current one closes

---

## Step 1: Create the milestone

When handed a set of goals (from brainstorming or direct description), create a GitHub milestone:

- Title: the name of the project or feature
- Description: one sentence on what this milestone delivers
- Due date: only if the user has stated one

State the milestone to the user and confirm before creating it.

---

## Step 2: Create issues for each goal

For each goal, create a GitHub issue on the milestone:

- Title: one clear sentence describing the goal
- Body: a checklist of the concrete steps to complete it
- Order by logical dependency — what must be done before what

State the ordered list to the user before creating anything. Do not create issues for speculative ideas — if something is uncertain, flag it and ask whether it belongs in the milestone.

**Confirm with the user before creating the issues.**

---

## Step 3: Work through issues in order

At the start of each session, surface the open issues on the current milestone. State which issue is next and confirm with the user before starting.

The goal is complete when every item in the issue checklist is done. Close the issue at that point.

---

## Step 4: New ideas during a session

When either the user or Claude thinks of something new mid-session:

1. Stop. Do not discuss how to implement it.
2. State: "This isn't in the current goal. I'm logging it as a new issue."
3. Create a new issue on the milestone with a brief description.
4. Return to the current goal.

The idea is preserved. It gets evaluated after the current goal is complete.

---

## Step 5: Reflection gate between goals

When an issue is closed, before opening the next one:

1. Show what was just completed.
2. Show the next issue in the queue.
3. Ask: "Does this still make sense to build, or has finishing the previous goal changed anything?"

Do not start the next issue until the user confirms it.

---

## Agents

Issues can be assigned to individual agents. Each agent works its assigned issue independently. An agent must not start work on an issue that isn't assigned to it.
