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
