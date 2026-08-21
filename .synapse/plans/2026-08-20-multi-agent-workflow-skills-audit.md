Multi-Agent Skills Audit — 2026-08-20

Scope

- Target: all files under /skills/ (skill guidance docs that drive agent behavior).
- Goal: find instructions or wording that would enable uncontrolled agent fanout or implicit passing of full conversational context; assess compliance with the retrospective rules (no implicit context passing, leader/worker pattern, spawn gating, spawn budget, and limited parallelism).
- Method: grep for spawn/subagent/context/transcript/conversation and read relevant skill files.

Summary (high level)

- Overall: the skill suite already contains strong guidance that matches the retrospective: many skills explicitly forbid passing full session history, require focused prompts, and limit when to spawn subagents.
- Risk surface: the guidance is mostly advisory. Without runtime enforcement or helper APIs, agents or implementers can still call spawn APIs and forward context. A few skills suggest spawning subagents in ways that are safe in principle but could be misused without enforcement.

Audit findings (per-skill)

1) skills/parallel-agents/SKILL.md
- Key lines:
  - "They must not inherit session history — give each exactly the context it needs."
  - "Fire in one response — multiple Task/subagent calls together = parallel."
- Assessment: Guidance is explicit about not inheriting session history and about focused prompts. Risk: Medium. Rationale: parallel fanout is explicitly allowed; if callers are careless they may still include large context in the prompt. Mitigation: require use of helper APIs that build compact artifact pointers instead of pasting transcripts.
- Suggested edits:
  - Add an explicit note: "Always pass file paths or artifact pointers; never paste the full transcript. Use agent-utils.atomic_dispatch() (TBD) to create per-worker briefs."
  - Provide a short template for the prompt payload: {task_id, repo_paths:[], error_snippets:[{path,lines}], constraints, expected_return}.

2) skills/subagent-team-execution/SKILL.md
- Key lines:
  - "Keep your context clean — hand requirements as files or tight prompts, not session history dumps."
  - "Do not paste accumulated prior-task histories."
- Assessment: Low risk. Rationale: explicitly prescribes handing requirements as files and warns against session history. However, implementers may ignore this without enforcement.
- Suggested edits:
  - Add file examples and small code snippet showing atomic read/modify/write of a task artifact and how to reply with a worker-specific result file.

3) skills/writing-specs/SKILL.md
- Key lines:
  - Agent produces a PENDING spec plus sibling .questions.json; "Do not conduct the interview in chat. Do not mark the spec APPROVED; the script owns that transition."
- Assessment: Low risk. Rationale: This skill already enforces separating drafting from interview and prevents agents from grabbing approval in chat.
- Suggested edits:
  - Cross-link templates in .synapse/templates and reference agent-utils helpers for writing artifacts atomically.

4) skills/executing-plans/SKILL.md
- Key lines:
  - "Use subagent-team-execution instead when tasks are independent and you want a fresh subagent per task." and general process guidance.
- Assessment: Low–Medium. Rationale: Execution guidance favors inline execution and uses subagents only in defined cases. Still advisory only.
- Suggested edits:
  - Add explicit spawn_limit recommendation for subagent-team-execution and recommend spawn_budget tokens for each subagent.

5) skills/debugging/SKILL.md
- Key lines:
  - "Never ask the user to repro something you can trigger yourself." and "Spawn an investigation pipeline of subagents for this" is in the DON’T list.
- Assessment: Low risk. Rationale: debugging skill explicitly forbids spawning investigation pipelines of subagents; this is aligned with retrospective.
- Suggested edits: none required; consider making the prohibition more prominent and machine-detectable.

6) skills/goal-oriented-development/SKILL.md
- Key lines:
  - "When the user has chosen an outcome to track, spawn a goal-writer agent (Task tool / subagent) with the stated intent and repository path."
  - "When the user explicitly asks for a broad assessment, spawn goal-surveyor with the repository path and their direction. It returns evidence plus questions or potential issue prompts. It does not create goals."
- Assessment: Medium. Rationale: This skill allows spawning when user-initiated — which is appropriate — but these spawned agents could themselves spawn others (e.g., goal-writer spawning codebase-explorer). That chain is acceptable when limited, but must be gated by leader semantics and budgets.
- Suggested edits:
  - Clarify that the initial spawn must include a spawn_budget_tokens field and that spawned agents must not spawn further subagents without recording a compact justification and checking the budget.
  - Add example of safe spawn payload (intent, repo_paths, task_id, spawn_budget_tokens).

7) skills/code-review/SKILL.md
- Key lines:
  - Mentions: "Does the reviewer have full context?" and warns about implementing without verification.
- Assessment: Low risk. Rationale: Mostly process guidance; no spawn patterns.
- Suggested edits: none immediate.

8) skills/thinking/SKILL.md
- Key lines:
  - "Do not create artifacts or make repository changes." and guidance separating thinking vs writing-specs.
- Assessment: Low risk. Rationale: Good separation of conversational exploration and artifact creation.
- Suggested edits: cross-link to writing-specs and to a standard artifact schema for questions/specs.

9) skills/README.md
- Key lines:
  - Suite-wide rules: thinking is read-only; writing-specs captures intent and TODO conducts terminal interview; neither skill automatically invokes the other.
- Assessment: Low risk. Rationale: High-level rules exist.
- Suggested edits: Add a short enforcement note: "Prefer agent-utils helpers; CI scans will flag direct transcript forwarding or spawn calls without spawn_budget." (once implemented)

Cross-cutting observations

- Guidance exists that discourages passing full transcripts and encourages file-based handoffs. This is strong; the retrospective proposals align well with current skills.
- The primary weakness is lack of enforcement: nothing in the skills themselves prevents an agent implementation or a Task/agent caller from passing the conversation history as a prompt when invoking multiple subagents.
- There is no explicit, cross-referenced spawn_budget or spawn_limit field in these skill docs today. The retrospective's artifact templates and helper APIs would close that gap.

Risk levels (aggregate)

- High risk: none found in skills docs alone. The risk is behavioral (implementations ignoring docs).
- Medium risk: skills that explicitly allow parallel dispatch or spawning (parallel-agents, subagent-team-execution, goal-oriented-development) because they create surfaces for fanout if misused.
- Low risk: writing-specs, debugging, executing-plans, thinking, code-review, and README contain safe guidance.

Recommendations (next actions)

1. Implement enforcement helpers (agent-utils) that provide atomic artifact writes, spawn validation (spawn_limit, spawn_budget), and cost logging. Make these helpers the canonical API agents use when dispatching subagents.
2. Add examples and small code snippets in the medium-risk skills showing safe usage of agent-utils (prompt templates, artifact pointers, spawn payload). Encourage using artifact pointers instead of pasting transcripts.
3. Add a lightweight CI lint or pre-commit hook that scans for risky patterns in agent code and skill docs: passing variables named `context`, `transcript`, `conversation` into spawn or Task calls; direct spawn calls without spawn_budget metadata; and agents invoking `spawn` outside leader-designated paths.
4. Produce migration guidance mapping common patterns to the safe APIs (example: replace spawn + full transcript with writing .synapse/tasks/<task-id>.json and then calling task helper to dispatch workers with that task_id).
5. Start with non-blocking CI warnings, then graduate to failure in branches that add new agent spawn code until teams have migrated.

Deliverable

- This audit has been saved to `.synapse/plans/2026-08-20-multi-agent-workflow-skills-audit.md` in the repo.

Prepared by: an AI assistant using Copilot CLI runtime in VS Code
