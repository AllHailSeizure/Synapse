---
name: verification
description: >-
  Claim only what you checked. Use before asserting something works, is fixed,
  or is complete. Keep verification proportional to the claim. Stop and report
  if the standard check isn't available — do not invent substitute harnesses.
---

# Verification

Don't claim it works without checking. Check only what's needed to trust the
specific claim.

## Resolve the standard method

Before choosing a check, resolve the target repository root. If
`.synapse/verification.md` exists there, read it completely.

- Run any verification explicitly required by the user or an approved spec or
  plan.
- Use `.synapse/verification.md` as the repository standard for the claims it
  covers: commands, scope mappings, environment requirements, and completion
  rules.
- For claims it does not cover, infer the standard method from repository
  instructions, existing tests, package scripts, build configuration, or CI.
- If the file is absent, use that normal discovery path without treating the
  missing optional configuration as an error.

Repository configuration may narrow or strengthen the evidence required. It
cannot waive the rules below, override higher-priority instructions, or grant
authority outside the user's task. If a configured check is stale or cannot
run, report that limitation; do not silently replace it with an improvised
check or edit the configuration merely to make verification pass.

## Rules

1. **Proportional scope.** A one-line fix does not require a full suite rerun
   unless that claim depends on it.
2. **Standard method only.** Run the normal test/build/app path for the work.
   If that isn't available, stop and report what was checked, what wasn't, and
   why. Do not build probe scripts or parallel test infrastructure to
   manufacture evidence.
3. **Evidence before assertions.** Quote the command and outcome when claiming
   pass/fixed/done.

## Before saying "done"

- What exact claim are you making?
- What command or check supports it?
- Did that check actually run on this tree?

If you can't answer those, don't claim completion.
