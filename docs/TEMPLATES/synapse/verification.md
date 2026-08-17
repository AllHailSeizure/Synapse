# .synapse/verification.md — template

Copy this to `.synapse/verification.md` in a repository where Synapse should
use project-specific verification instructions. Only the `verification` skill
reads this file.

Describe the repository's standard, direct methods. Keep commands literal and
completion rules observable. This file may strengthen or narrow the evidence
needed for a claim; it cannot waive Synapse's evidence rules or authorize work
outside the user's request.

Delete entries that do not apply. An absent file or uncovered claim falls back
to the repository's documented tests, package scripts, build configuration,
app path, or CI conventions. A configured command that is stale or unavailable
is reported, not silently replaced with an improvised harness.

---

## Standard checks

- Focused tests: `<command and required arguments>`
- Full test suite: `<command and required arguments>`
- Build: `<command and required arguments>`
- Lint/typecheck: `<command and required arguments>`

## Scope mapping

- Changes under `<path or component>`: run `<check>`
- Changes under `<path or component>`: run `<check>` and manually inspect
  `<observable behavior>`
- Documentation-only changes: `<check or explicit no-runtime-check rule>`

## Environment requirements

- Required runtime/version: `<literal requirement>`
- Required services or applications: `<literal requirement>`
- Checks unavailable in CI or headless environments: `<check and reason>`

## Completion rules

- “Focused tests pass” requires: `<observable evidence>`
- “Build succeeds” requires: `<observable evidence>`
- “Feature works” requires: `<automated and/or manual observable evidence>`
