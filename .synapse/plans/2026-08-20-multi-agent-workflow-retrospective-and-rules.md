Retrospective: 2026-08-20 — Multi-Agent Fanout and Token Expenditure

Summary

An observed incident: an autonomous agent fanout pattern caused a large uncontrolled number of model calls by repeatedly spawning peer agents and passing full conversational context to each. This resulted in excessive token usage and cost.

Goal

Define practical, repository-level rules and a small implementation plan to prevent uncontrolled fanout and stop passing large conversational context blobs between agents.

Immediate Rules (high priority)

1. No implicit context passing
   - Agents must never forward the entire chat transcript or large context blobs to another agent. Instead, agents must write a compact, machine-readable artifact to the repository (JSON/YAML/TOML) containing only the necessary state, references, and pointers.

2. Single-writer artifacts
   - Use a single authoritative artifact per task (e.g., `.synapse/tasks/<task-id>.json`). Agents must append or atomically update this artifact; do not pass state via agent-to-agent messages.

3. Leader/coordinator pattern for delegation
   - Only a designated leader agent (or the human operator) may decide to spawn additional agents. Worker agents are single-purpose: they read the artifact, act, and write results back. They do not spawn other agents.

4. Explicit spawn gating and budget
   - Every spawn decision requires (a) explicit justification in the leader's log, and (b) a token budget for the work. The leader must compute and record an estimated token budget in the task artifact before spawning.

5. Parallelism limits
   - Limit concurrent workers per leader to a configurable N (default: 3). The leader must wait for worker completions or timeouts before creating more workers.

6. Machine-readable question files instead of chat context
   - When a draft requires human decisions, the agent emits a sibling questions file alongside the artifact (e.g., `.synapse/specs/<name>.questions.json`). The CLI or operator supplies answers; no agent should conduct that interview automatically.

7. Observability and cost accounting
   - Agents must log each model call to a local cost log (timestamp, agent-id, model, prompt size tokens, response size tokens, estimated token cost). Periodic audits should summarize total spend per task and per leader.

8. Fail-safe defaults
   - If a leader cannot justify a spawn or the token budget is missing, refuse to spawn and surface the reason as a task artifact field.

Implementation plan (minimal changes first)

Phase 1 — Policy artifacts and docs (today)
- Add this retrospective/rules file under `.synapse/plans/` (this file).
- Add a short example artifact template under `.synapse/templates/` (task.json + questions.json).
- Add guidance to `skills/parallel-agents/SKILL.md` (or create it) summarizing the leader/worker pattern and explicit gating.

Phase 2 — Instrumentation and thin helpers
- Add a small helper library (scripts/agent-utils.py or .ps1) used by agents to: read/write task artifacts atomically, append cost-log entries, and enforce spawn limits. Keep it dependency-light.
- Add a Git hook or CI lint that scans PRs/agent code for obvious context-forwarding patterns (search for `context` or `transcript` usage in agent spawn calls) and warns.

Phase 3 — Enforcement and tests
- Add unit tests for the helper library's atomic write and budget gating behavior.
- Add a smoke test that simulates leader spawning workers limited by the parallelism cap.

Phase 4 — Operator workflows and training
- Update `AGENTS.md` and relevant `skills/*` docs with clear examples: spec-writer + CLI pattern (no chat approval), leader spawns workers with an artifact, workers write results back.
- Run a small training/doc session for operators on the new flow.

Artifact templates (examples)

- `.synapse/tasks/<task-id>.json` (minimal fields)
{
  "task_id": "<uuid>",
  "leader": "agent/identifier",
  "status": "pending",  // pending | running | complete | failed
  "spawn_budget_tokens": 2000,
  "spawn_limit": 3,
  "worker_ids": [],
  "log": []
}

- `.synapse/specs/<name>.questions.json`
[
  {"id":"q1","prompt":"Which behavior should be default?","options":["A","B"],"recommended":"A"}
]

Next steps for the repo

1. Confirm desired defaults for spawn_limit and default token budget.
2. Create the small helper scripts and the template files.
3. Update or create a `skills/parallel-agents/SKILL.md` doc describing the leader/worker pattern and linking to these templates.
4. Optionally add a lightweight CI scan that warns on context-forwarding patterns.

If this direction looks correct, proceed to create the template files and add the `skills/parallel-agents/SKILL.md` guidance and a minimal helper script for atomic artifact writes and token logging.
