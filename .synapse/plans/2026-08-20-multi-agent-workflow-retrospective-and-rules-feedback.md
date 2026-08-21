Audit Feedback — Multi-Agent Fanout Retrospective (2026-08-20)

Short answer

The retrospective's proposals are sensible and will help significantly, but they need clearer enforcement and some additional safeguards to be reliable in practice.

Why these proposals will help

- They block the main vector for runaway token usage by prohibiting implicit context forwarding.
- Machine-readable artifacts (task/spec/question files) create deterministic handoffs and make agent work auditable and reproducible.
- The leader/coordinator pattern restricts who may spawn workers, reducing accidental fanouts.
- Token budgets and spawn limits provide controllable cost boundaries.
- Question files and a CLI interview place approval authority with humans, not agents.

Gaps and risks (what to watch for)

1. Enforcement vs. guidance
   - Doc-level rules alone won't stop buggy agents. Without tooling to enforce or flag violations, agents will continue to spawn and forward context. Add a helper library and CI/pre-commit checks to detect and prevent risky patterns.

2. Race conditions and atomicity
   - Concurrent workers writing the same artifact can cause lost updates or conflicts. Implement atomic read/modify/write helpers, append-only logs, or a single-writer enforcement pattern. Provide safe helper APIs for agents to use.

3. Token-budget estimation and gaming
   - Pre-computed token budgets are heuristics and can be inaccurate. Use conservative defaults, allow explicit emergency overruns with justification, and record actual vs estimated to improve heuristics.

4. Migration friction
   - Existing agents likely assume chat transcripts and ad-hoc spawning. Migration will require effort and tests. Offer templates, helper APIs, and a compatibility lint to ease incremental migration.

5. Security and integrity
   - Agents writing to the repo could corrupt files. Restrict agent writes to designated .synapse subfolders and consider signed artifacts or access control for which agent IDs may modify which tasks.

6. Observability overhead and privacy
   - Log metadata (agent-id, model, tokens-in, tokens-out, timestamp, brief hash) instead of full transcripts by default. Make full transcript logging opt-in and access-controlled.

Concrete additions to strengthen the retrospective

- agent-utils helper library that provides:
  - Atomic read/write helpers for .synapse task artifacts.
  - Cost-log append helper to record token usage.
  - Spawn validation that enforces spawn_limit and spawn_budget before allowing spawn calls.

- A CI check or pre-commit hook that scans for:
  - Direct use of variables named context, transcript, or similar being forwarded into spawn calls.
  - Spawn API calls originating from non-leader code paths.

- Clear examples and templates demonstrating the leader/worker pattern:
  - Leader writes the task artifact with spawn_budget and spawn_limit and a justification log entry.
  - Worker reads the artifact, performs work, writes results to a worker-specific path, and appends to the task log.

- Tests:
  - Unit tests for atomic helpers and spawn validation.
  - Integration smoke test that simulates leader spawning workers and enforces spawn_limit.

- Migration guidance documenting how to convert existing agents to the leader/worker model.

Bottom line

- The retrospective is on the right track: it will reduce accidental token blow-ups if implemented with enforcement and safeguards.
- The most important missing pieces are enforcement (tooling and CI) and concrete helper APIs that make the safe pattern the path of least resistance.

Recommended next step

Produce a targeted audit of the repo to find current risky patterns (spawn points, context forwarding) and produce exact edit suggestions where needed. That audit will show how invasive migration will be and where to prioritize helper APIs and CI checks.

Prepared by: an AI assistant using Copilot CLI runtime in VS Code
