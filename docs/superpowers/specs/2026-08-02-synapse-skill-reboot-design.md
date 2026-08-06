# Synapse Skill Reboot — Design

## Context

Synapse was built after a few weeks of AI-assisted coding. Two months and a
lot more experience later, the original design over-applies ceremony: fixed
hard gates fire on every task regardless of size, the code-review and
verification skills spiral into open-ended loops, and comments bloat trivial
diffs. This design reboots Synapse's skill set — largely by adopting and
customizing skills from the `superpowers` plugin, which already covers much
of the same ground (brainstorming, plans, TDD, git worktrees, subagent
orchestration, code review, verification) — rather than rebuilding
everything from scratch.

## Rejected approach: a formal triage/classification model

An early draft of this design proposed a "root philosophy" rewrite of
`CLAUDE.md`: classify every task into named complexity tiers (Trivial /
Standard / Complex) and let the tier dictate how much process applies.

This was explicitly rejected mid-design. Building a classification ceremony
to decide when ceremony applies is the same failure mode this reboot exists
to fix — it just moved the over-engineering up one level. The resolution:
**no named tiers, no forced classification step.** Judgment is trusted
per-decision, using concrete risk questions (is this hard to reverse? does
it touch a shared/critical path? is there real ambiguity? does it set a
pattern other code will follow?) as triggers for *that specific decision* —
never as inputs to a label slapped on the whole task. Most of the actual
grievances behind this reboot are better fixed as direct, concrete
corrections than as a new abstraction, which is what the rest of this
document does.

## Superpowers skill audit

Decision made skill-by-skill, matched to Synapse's existing naming
conventions. Renames drop Superpowers' verb-first gerund style
(`using-git-worktrees`, `dispatching-parallel-agents`) in favor of Synapse's
shorter noun-phrase style (`worktrees`, `parallel-agents`).

### Keep as-is

- **`brainstorming`** — this process itself.
- **`writing-plans`**, **`executing-plans`** — the planning half of the
  workflow; not a source of complaints.
- **`worktrees`** (from `using-git-worktrees`) — already mechanical, not
  ceremony-heavy: detect existing isolation → native tool → git fallback →
  project setup → baseline test check. Also the base mechanic the PR-stacking
  workflow (see Open Follow-ups) will build on.
- **`parallel-agents`** (from `dispatching-parallel-agents`) — already a
  clean decision tree (independent problems → parallel dispatch; related →
  investigate together) with no menu and no waiting on the user. Matches
  "delegate subagent-vs-inline to me" directly; it already works that way.

### Adapt

- **`subagent-team-execution`** (trimmed from `subagent-driven-development`)
  — keep the parts that already match what was asked for: fresh subagent per
  task, narrate at most one line, continuous execution without pausing to
  check in between tasks. Cut the internal review machine: no mandatory
  task-reviewer subagent after every task, no 5-round fix loop, no ledger
  bureaucracy, no final whole-branch reviewer dispatch. This internal loop is
  the likely source of runaway verification sessions. Real review now
  happens once, externally, when the PR goes up (see `finishing-branches`
  and the git hook below).

- **`testing`** (trimmed from `test-driven-development`, replaces
  `testing-preferences`) — keep red-green-refactor as the good default
  mechanic for real feature/bugfix work. Cut the "Iron Law," the
  mandatory-delete-and-restart-on-any-deviation framing, and the
  ask-permission-for-exceptions rule. Aligns with Synapse's existing baseline
  testing philosophy ("verification-first when behavior is clear, TDD when
  exploring design") instead of contradicting it.

- **`verification`** (trimmed from `verification-before-completion`) — keep
  the core principle: don't claim something works without having checked.
  Cut the "Iron Law" absolutism and the blanket requirement to re-verify
  everything before any positive statement. Add two concrete constraints
  that came out of this design session:

  1. **Proportional scope.** Verify what's needed to trust the *specific
     claim* being made. Don't re-run a full suite or rebuild test
     infrastructure to confirm a small, low-risk change.
  2. **No substitute verification infrastructure.** *"If the standard,
     simple verification method isn't available, stop and report what you
     have to Nate."* Verify with the standard, direct method for the work at
     hand — run the tests, run the build, run the app. If that direct method
     isn't available (can't run the engine, no environment, no access),
     that's the stopping point: report exactly what was checked, what
     wasn't, and why — and hand the decision back. Do not invent a
     substitute (probe scripts, synthetic harnesses, parallel test
     infrastructure) to manufacture evidence the standard method couldn't
     produce. This directly targets a repeated failure mode: an entire
     session spent building custom verification tooling (e.g. ad-hoc probes
     for an engine that couldn't be run directly) that produced far more
     test code than production code.

- **`code-review`** (trimmed from `receiving-code-review`, replaces
  `code-review-standards`) — kept close to as-is; it was never the ceremony
  problem. "Verify before implementing, no performative agreement, push back
  with technical reasoning if wrong" is good practice as written. Re-scoped
  trigger: fires when automated PR review feedback lands (via the git hook
  below), not from an internal request/response dance.

- **`finishing-branches`** (adapted from `finishing-a-development-branch`) —
  today: verify tests → present a 3-option menu (merge / PR / keep) → wait
  for the user, every time. New behavior: verify tests → resolve base branch
  (previous branch in the stack, if stacked; otherwise the usual base) →
  push and open the PR, posting a non-blocking one-line heads-up ("Pushing
  PR #X against `<branch>`") rather than a menu that blocks on a reply.
  Merge-to-base and discard remain explicit, user-initiated actions — those
  are the genuinely hard-to-reverse decisions and stay gated.

### Drop

- **`requesting-code-review`** — this was the internal "dispatch a reviewer
  subagent, mandatory after every task/feature/before merge" half of the
  review loop. Superseded entirely by the external git-hook-driven review
  described above.
- **`writing-skills`** — Nate already prefers Anthropic's `/skill-creator`
  plugin for authoring/editing skills (existing memory:
  `feedback_skill_creator.md`).

## Open follow-ups (not detailed in this spec)

These were directionally agreed during this session but need their own
spec/plan cycle before implementation:

1. **`goal-oriented-development` v2** — goal-writer records intent only (not
   a prescribed solution); the primary session triages each issue (dispatch
   an agent for simple work, brainstorm with Nate for anything non-trivial),
   then chooses orchestration (the `subagent-team-execution` skill above, or
   inline work) itself. Builds directly on the in-progress
   `feat/workflow-reorientation` branch, which already reworked the
   goal-writer/goal-fulfiller split in this direction.
2. **PR-stacking mechanics** — how a stack of worktree-based branches tracks
   its dependency order (which branch is whose base), beyond the
   `finishing-branches` behavior already agreed above.
2a. **Worktree/branch cleanup on merge** — a QOL request from Nate: when a
   branch merges (anywhere in a stack), automatically remove its worktree
   and delete the branch. Resolved as two independent mechanisms, both
   deliberately separate from Claude Code:
   - **Remote branch:** enable GitHub's native "Automatically delete head
     branches" repository setting. No custom code — this is a server-side,
     instant-on-merge action GitHub already provides.
   - **Local worktree + local branch:** GitHub cannot reach Nate's
     filesystem, so something local has to notice the merge. Chosen
     mechanism: a `post-checkout`/`post-merge` git hook, tracked in a
     `.githooks/` directory and wired in via `core.hooksPath`, that fires on
     routine local git activity (pull, checkout) and checks each worktree
     branch with `gh pr view <branch> --json state` — merged branches get
     their worktree removed (`git worktree remove`) and the local branch
     deleted (`git branch -d`). Not instant, but self-triggering with no
     standing background process. Still needs its own implementation plan
     (hook script contents, `.githooks/` setup, documenting the one-time
     `core.hooksPath` config step).
3. **Comment discipline** — Nate flagged persistent over-commenting (e.g. 10
   lines of comments on a 1-line change) as a real problem. The existing
   `CLAUDE.md` rule ("default to no comments; only add when the WHY is
   non-obvious") already says the right thing but evidently isn't holding in
   practice. Needs a concrete enforcement mechanism, not just a restated
   rule — possibly a self-review pass (the existing `simplify` skill may
   already cover this) rather than a new skill.

## Post-review updates

Feedback from Nate's review of this spec, applied directly since each item
was concrete and low-risk:

- **`speccing-first` removed.** It no longer exists as a concept in
  Synapse — not just the missing skill file, but its references in
  `CLAUDE.md` (the "Spec before code" step in "How We Work Together" and its
  line in the Skills list) and `README.md` (its inventory entry, its line in
  "How the skills chain," and its entry in the repository-structure
  listing). Edits applied directly to both files.
- **PR template added** at `.github/PULL_REQUEST_TEMPLATE.md`: summary,
  issue linking (`Closes #` / `References #`), a stack section (base branch,
  explicit note that stack PRs merge only on Nate's go-ahead, never
  auto-merged), and a labels section referencing the type/priority taxonomy
  already established in `ref/labels.json` on `feat/workflow-reorientation`
  (`feat`/`fix`/`refactor`/`test`/`docs`/`tooling`/`assets` +
  `priority:high/medium/low`). Labels themselves are applied via
  `gh pr create --label`, not the template body.
- **Stacked PRs never auto-merge.** `finishing-branches` opens each PR in
  the stack (auto-pushed, non-blocking heads-up, as already designed above)
  and stops there. Merging — of any PR in a stack, at any position — is
  always Nate's explicit action, never automatic, regardless of what the
  git-hook-driven review reports. This is now folded into the
  `finishing-branches` adaptation, not just the open PR-stacking follow-up.

## Non-goals

- No formal task-classification/triage system (see Rejected approach,
  above).
