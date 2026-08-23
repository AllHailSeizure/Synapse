Global Agent Coordination & Anti-Fanout Proposal

Prepared for: platform owners, agent runtime maintainers, and repository maintainers
Prepared by: an AI assistant using Copilot CLI runtime in VS Code
Date: 2026-08-21

Purpose

Provide a short, practical proposal to stop runaway agent fanout and uncontrolled token expenditure across agents, repositories, and platforms. This is an architecture and rollout plan designed for ecosystem adoption, not just a single-repo mitigation.

Key ideas (tl;dr)

- Standardize a tiny Agent Coordination Artifact (ACA) schema that records task_id, leader identity, spawn_budget_tokens, spawn_limit, allowed paths, and an audit pointer.
- Ship portable agent-utils helpers (Python + CLI + PowerShell) so authors use safe primitives instead of forwarding full transcripts.
- Offer a coordinator signing/endorsement service for agents/runtimes that lack repo access; endorsements let runtimes validate spawn approval without repository reads.
- Push runtime interceptors into cooperating agent platforms that block/require an ACA or signed endorsement before allowing spawn calls that pass non-trivial context or create multiple workers.
- Use provider-level quotas and alerting as defense-in-depth.

Why this is necessary

- Repo-side docs and patterns are helpful but insufficient. Agents run in diverse runtimes (local, hosted, cloud); enforcement needs platform participation to be comprehensive.
- An explicit, machine-verifiable contract (ACA) lets runtimes make deterministic decisions: reject blind fanout, enforce budgets, and audit spend.

Architecture overview

1) ACA (Agent Coordination Artifact)
- A small JSON artifact with keys: version, task_id, leader, spawn_budget_tokens, spawn_limit, allowed_paths, metadata, leader_signature (optional), audit_log.
- Stored under .synapse/tasks/<task-id>/artifact.json or produced and signed by a coordinator.
- Purpose: canonical, auditable justification for spawning workers.

2) agent-utils (reference helpers)
- Functions: create/read/atomic_update ACA, validate_spawn, reserve_spawn_budget, record_worker_result, append_cost_log, compact_brief_from_files.
- CLI & PowerShell shim so any runtime can use it without installing packages.
- Default behavior: do not record full prompts; cost logs contain token counts and optional hashes only.

3) Coordinator / endorsement service (reference)
- Optional network service that signs ACA artifacts and issues short-lived endorsement tokens.
- Enables enforcement for cloud or hosted agents that cannot access repo files.
- Simple REST endpoints: sign(artifact) -> token; verify(token) -> artifact metadata.

4) Runtime interceptors
- Platforms add a check on spawn/subagent calls: if the spawn includes non-trivial conversational context or requests parallel workers, require either a local ACA artifact or a coordinator endorsement token.
- If missing or budget/limit exceeded, block or escalate to human confirmation.

5) Provider controls
- Model and platform providers should offer per-agent and org-level quotas, rate-limits, and rapid alerts for abnormal fanout patterns.

Operational details

- Cost logging: .synapse/tasks/<task-id>/cost.log as newline-delimited JSON entries: {ts, agent, model, tokens_in, tokens_out, prompt_hash?}
- Atomic updates: helper provides a file-lock pattern and atomic replace semantics compatible with Windows and POSIX.
- Privacy: default logs avoid raw prompt text; full transcripts opt-in, access-controlled.

Phased rollout

Phase A: Publish spec and helpers
- Publish ACA JSON schema and agent-utils (Python + CLI + PS shim) as reference.
- Provide templates, skill doc updates, and MIGRATION.md examples.
- Encourage repo owners to adopt helpers and add CI warning checks.

Phase B: Warning & telemetry
- CI non-blocking checks flag context forwarding and missing ACA usage.
- Platforms emit telemetry for spawn operations lacking ACA/endorsement.

Phase C: Runtime enforcement (cooperating platforms)
- Platforms block spawn calls that would fail ACA checks; require coordinator endorsements when repo access is unavailable.
- Providers enable quotas and alerts.

Phase D: Ecosystem adoption
- Increase enforcement coverage, expand coordinator adoption, and adjust provider quotas based on observed patterns.

Example flows (compact)

Leader:
- agent-utils create-task --task-id T1 --leader L --spawn-budget 2000 --spawn-limit 3
- write compact brief pointing at files/paths (no full transcript)
- agent-utils reserve-spawn --task-id T1 --tokens 500 --worker-ids w1 w2
- spawn workers with payload {task_id:T1, worker_id:w1, brief_ref:...}

Worker:
- agent-utils read-task T1
- run work with only brief and referenced files
- agent-utils record-result --task-id T1 --worker-id w1 --summary "..."
- agent-utils append-cost --task-id T1 --agent-id w1 --model gptX --tokens-in N --tokens-out M

Risks & mitigations

- False positives: grep-based CI may catch benign patterns; tune rules and start with warnings.
- Non-cooperating runtimes: provider quotas and telemetry limit damage and help trace incidents.
- Migration friction: provide clear migration examples and a coordinator signing path for backward compatibility.

Next recommended actions (practical)

1. Publish ACA schema and artifact template in a public place (repo and a short RFC).
2. Harden agent-utils (timezone-aware datetimes, unit tests, packaging) and publish the reference implementation.
3. Create CI warning scripts and include them in a starter GitHub Action for any repo to adopt.
4. Engage major runtimes/platforms to pilot runtime interceptors and endorse the coordinator model.
5. Ask major model providers to expose per-agent quotas and alerting for abnormal fanout.

If useful, I can:
- Draft the ACA RFC and a short public Markdown RFC for outreach.
- Implement unit tests and a small coordinator reference service prototype.

Which of these would you like next?