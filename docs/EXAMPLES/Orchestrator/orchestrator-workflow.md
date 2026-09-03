# Orchestrator Workflow — as practiced, 2026-08-18

Notes toward a skill. Written from one session that worked: a verbal brain-dump of eight
half-formed TODOs turned into eight merged PRs, two implementation-plan sets, and a settled
architecture decision, without the user having to hold any of it in their head.

This is not "spawn agents to go faster." It's a division of labour where the orchestrator keeps
everything that is *irreversible, unverified, or the user's to decide*, and delegates everything
that is *bounded and reconstructible*.

---

## 1. The shape

**Orchestrator** stays in the main checkout. It triages, dispatches, verifies claims, relays
results, and owns anything risky. It does not implement bounded work itself.

**Workers** get one worktree each, one task, and a self-contained brief. They commit, push, open a
PR, and stop. They never merge.

**The user** answers only what genuinely requires them, batched, at moments they choose.

The failure mode this avoids isn't slowness — it's the user becoming the integration point for
their own project, having to hold context for every parallel thread.

---

## 2. Triage before dispatch, always

Given a list, resist the urge to start. Spend the first pass classifying:

| Class | Handling |
|---|---|
| Independent, bounded | Dispatch immediately, in parallel |
| Blocked on another item | Hold, name the blocker |
| Needs a decision only the user can make | Ask — but batch it, don't block on it |
| Touches the dirty working tree | **Orchestrator only.** Not delegatable |
| Already done | Check before building |

That last row earns its place. In this session one of the eight items was already merged weeks
prior. The dispatched agent found it in 78 seconds and stopped rather than duplicating it. **Brief
agents to check for existing work first and to stop if they find it** — a worker that reports "this
exists, here's the evidence, I did nothing" is a success.

---

## 3. What the orchestrator must not delegate

**Anything in the main checkout's uncommitted state.** A worktree branches from HEAD. It cannot see
uncommitted or untracked files. If the task is "sort out this dirty tree," that is structurally
un-delegatable.

**Anything destructive or irreversible.** Splitting a user's uncommitted art across branches is the
canonical example. Get it wrong and the work is gone with no git-recoverable trace.

**The procedure that worked for the risky case:**

1. Back up every dirty and untracked file to a scratch directory *before touching anything*.
2. Commit everything to branches. Additive only. Nothing reverted yet.
3. Verify each committed blob hashes identical to the backup.
4. Only then clean the working tree.
5. Re-verify after any later merge or rebase touches those branches.

Step 3 is what makes step 4 safe to do without asking. Doing it in the other order means asking
permission for every step, which defeats the point.

---

## 4. Briefs are the whole game

A worker starts cold. Everything it needs must be in the brief. What consistently mattered:

- **State the authority.** Which file is the source of truth, and that it *is* the source of truth.
- **Restate the project's hard rules inline.** Workers do not reliably absorb a root `AGENTS.md`.
  The rules that were restated got followed; assume the ones that aren't, won't be.
- **Name the anti-goal.** "Do not invent dialogue" prevented the single worst possible outcome in a
  creative project. Say what must not happen, not just what must.
- **Pre-empt known bad habits.** "Do not add tests as a side effect" and "do not modify art" were
  worth a line each every time.
- **Give current state, including what changed since the spec was written.** Specs go stale within
  days on an active project. Tell the worker which of the spec's stated blockers are now unblocked.
- **Hand over judgment explicitly, with the criteria.** "Decide between (a) and (b), prefer the more
  composable unless the code says otherwise, justify it in your report" produced a better answer
  than dictating a design would have.
- **Say where to branch from.** Work that depends on unmerged art must branch from the branch
  carrying it.
- **End with what to report.** Ask for the sequence, the judgment calls, the gaps, and the decisions
  needed — not a summary.

**A brief that names a file the worker cannot see is the most dangerous brief you can write.** It
happened here: the source-of-truth file was untracked, so it did not exist in the worker's worktree.
A worker told to transcribe from a missing file is one step from inventing the content. Check that
every file you cite is *tracked* before dispatching, and if it isn't, copy it into the worktree and
message the worker.

---

## 5. Verify claims; don't re-run work

Subagent reports are hypotheses. But re-running a worker's test suite wastes the delegation.

**The line that worked:** trust reported *test results*; verify reported *claims about the codebase*
— especially any claim that changes priorities or that you're about to relay to the user as fact.

Verification is usually one grep. In this session:

- "Chapter 4 has no follow variables" → confirmed, 0 occurrences vs 34 in Chapter 3. Real bug, and
  it meant a beat the spec called *built* had never worked.
- "`walk_to_and_lock` has four callers in these files" → **wrong.** Two cited files had zero
  occurrences; a real caller in shared infrastructure was missed. That error would have made a
  planned deletion task much larger than advertised.

One of those was right, one was wrong, and both mattered. Two greps.

**Also verify your own claims before relaying them.** Misreading a pre-existing failure as your own
fallout, or as the worker's, sends everyone down the wrong path. Isolate: does it fail without the
change?

---

## 6. Decisions: batch, and let the user set the interview

Fifteen open decisions accumulated across two plans. Dumping them as they arose would have been
useless. What worked:

1. Collect them from the plan documents rather than from memory.
2. Group by *kind*: creative (the user's alone), feel/fidelity, architecture, bookkeeping.
3. One or two lines each — the decision and the consequence, not the analysis.
4. Give a recommendation where you have one; say "reversible, proceeding" where it doesn't need them.
5. Let the user answer all at once, and let them ask for clarification item by item.

**When a user asks for clarification, they are not asking you to repeat the question.** They're
telling you the question was framed in mechanism instead of consequence. Re-frame in terms of what
happens in the game, not what happens in the code. "Should `LeaveParty` replace the dismissal?" is a
bad question. "When CV and Flo leave the party, should the player see them disappear?" is the same
question, answerable.

**Be willing to discover the question was wrong.** One decision here was framed as "is this
on-screen pop intended?" — the real answer was that every departure is authored choreography and the
question rested on a false premise. Withdraw and correct rather than extracting an answer to a
malformed question.

---

## 7. Push back once, with evidence, then follow

An agent recommended making story flags clearable. The right move was to disagree — with the
specific reason that milestones never need clearing, and that the thing driving the request wasn't a
flag at all — and then let the user reason to their own conclusion. They got there in one message
and stated it better than the analysis had ("you don't progress backwards through the story").

The value wasn't the recommendation. It was surfacing the actual shape of the problem and then
getting out of the way.

---

## 8. Reversibility governs how much you ask

Ask about creative content, product behavior, and anything irreversible. Decide and report on
technical choices confined to one module. Say which you're doing.

"This is a reversible technical choice, confined to E1, I picked X and here's why, proceeding unless
you object" is a complete handling. It respects the user's attention without hiding the decision.

---

## 9. What went wrong, and how each got turned around

These are the load-bearing part. None of them were caught by being careful up front — each was
caught mid-flight and converted, and the conversion is the pattern worth reproducing.

**Response length — caught by the user, twice.**

*What went wrong:* four-paragraph answers to one-line questions. A standing instruction to be
succinct was being satisfied on the letter (prose, not bullets) while missing the point entirely.
The user said the responses "only serve to obfuscate your meaning," and then had to say it again.

*How it turned around:* owning it as a misread rather than blaming the instruction, then actually
changing — three-sentence answers, one question at a time. What followed was the most productive
stretch of the session: the entire ActorManager design got settled in about ten short exchanges,
because each one was small enough to react to. **The long answers weren't just annoying, they were
blocking the design conversation.** Brevity wasn't a style preference, it was what made
collaborative thinking possible.

*Encode:* when a user corrects your output twice, stop defending the first correction and change
the behavior. And treat a standing brevity instruction as being about the reader's comprehension,
not about formatting.

**Assuming six CI failures were six problems.**

*What went wrong:* six PRs failed at once. The instinct — and the near-miss — was to start
debugging six branches.

*How it turned around:* reading one actual log instead of guessing, noticing all six failed on the
identical test, and then noticing the one PR that passed had a *later* run timestamp. The fix had
merged to master after those runs, and CI evaluates each PR as branch-merged-into-base. Every
failure was stale. Resolution was mechanical: merge master into each branch, push, all green.

*Encode:* **when many PRs fail identically, suspect shared base state before suspecting the
branches.** A passing sibling with a later timestamp is the tell. Read one log before forming any
theory.

**Briefing a worker on a file it could not see.**

*What went wrong:* the source-of-truth dialogue script was untracked, so it did not exist in the
worker's worktree. The worker had been told to transcribe from it verbatim, in a project whose
single worst failure mode is inventing dialogue.

*How it turned around:* catching it while the agent was still running — during unrelated work, by
noticing the file in `git status` as untracked — copying it into the worktree, and sending a
correction telling the worker to discard anything built from inference and confirm in its report
whether it had produced content yet. It hadn't; it had read the file from the main checkout by
absolute path and md5-verified the copy matched.

*Encode:* verify every file you cite is *tracked* before dispatching. And when you catch a bad
brief mid-flight, **send the correction immediately with an explicit instruction to discard
inferred work** — don't wait for the report. Ask the worker to confirm what it had already produced,
so you know whether the near-miss was a miss.

**The common thread.** All three were caught by noticing something in passing rather than by
checking a list: a `git status` line, a timestamp, a repeated complaint. The workflow's real safety
property isn't front-loaded rigor — it's that the orchestrator stays close enough to the work to
notice, and treats correction as routine rather than as failure.

---

## 10. Minimum viable version

If this becomes a skill, the irreducible core:

1. Triage the list; classify by dependency and delegability.
2. Keep dirty-tree and irreversible work; dispatch the rest, one worktree each.
3. Write briefs that carry authority, hard rules, anti-goals, current state, and a report contract.
4. Verify claims about the codebase; trust reported test runs.
5. Batch decisions; frame them in consequences; re-frame on request.
6. Never merge. Never decide the user's creative questions. Report gaps honestly.
