# Systematic Debugging Skill — Design Spec

## Motivation

`goal-oriented-development` proved that investing heavily in a multi-subagent
skill structure — front-loaded research, separated from structuring, separated
from execution — produces results that plain conversational prompting can't:
a chaotic project decomposed into 10+ well-formed issues across two
milestones, with essentially no hand-holding.

This spec applies the same investment to debugging. `systematic-debugging` is
named in root `CLAUDE.md` and tracked as issue #11, but no implementation
exists yet — this is a from-scratch build in the goal-oriented-development
style, not a refactor.

The design specifically targets two recurring pain points:

1. **Self-declared "fixed" that isn't.** When the same agent that writes a
   fix also judges whether it worked, self-report is unreliable. Verification
   must be a separate, independent step.
2. **Debugging deserves the same rigor as this project's testing philosophy**
   (see `testing-preferences`) — every line is a potential edge case — but
   that rigor shouldn't have to be supplied by hand each session. It should
   be structural.

## Scope

In scope: the investigation → verification pipeline for a single reported bug,
its agents, its artifacts, and its exit conditions (fixed, or a decision point
handed back to the user).

Out of scope (see Open Questions): the exact mechanics of non-automated
(manual/live-environment) reproduction and verification. V1 assumes an
automated repro (a failing test or script) is achievable; see below.

## Trigger Conditions

Mirrors goal-oriented-development's explicit trigger list in the skill
frontmatter `description`. Fires on:

- A bug report ("this is broken", "X isn't working")
- A failing test
- An error message or stack trace
- Unexpected behavior flagged by the user, even without a hard error

**Interaction with goal-oriented-development:** if a bug surfaces mid-goal,
systematic-debugging takes over the investigation. Once verified, the fix
becomes a completed checklist item on the *current* goal — it does not spin
off as a separate goal. The exception is if escalation caps out unresolved
(see Decision Point below): that produces its own GitHub issue, separate from
the active milestone.

## Pipeline Architecture

```
Round 1 (parallel):
  Internal Investigator ──┐
  External Researcher ────┤
                           ▼
                    Skeptic Gate
                     /         \
              survives          refuted
                 │                 │
                 ▼                 ▼
          Fix-Implementer    Escalate: parallel investigators
                 │            on alternate hypotheses
                 ▼            (informed by ruled-out list,
        Independent Verifier   so no dead end repeats)
                 │                 │
                 ▼                 ▼
            Final Report      Skeptic Gate (same as above)
                                   │
                        (after cap rounds, still refuted)
                                   ▼
                            Decision Point → user
```

## Agents

### Internal Investigator
Reproduces the bug, gathers evidence (code, logs, stack traces), and returns:
- A ruled-out list entry for anything it eliminates during its own search
- One leading code-level hypothesis, with supporting evidence and confidence
- Whether a reliable automated repro (test/script) could be built

If no reliable repro can be built, this is flagged immediately — nothing
downstream can be mechanically verified without one (see Open Questions).

### External Researcher
Runs in parallel with the Internal Investigator from round 1, not just on
escalation. Searches issue trackers, changelogs, and discussions for the
specific error against the *exact* dependency/framework versions in play.
Returns a candidate "known issue" hypothesis if found, with source (issue
link, version match details) — otherwise returns nothing.

This lens exists because "it's not us, it's them" is sometimes true and can
save hours (e.g. a known upstream bug in a specific framework version), but
is also the easy, comfortable answer to reach for — hence the asymmetric
skeptic bar below.

### Skeptic
Takes every hypothesis produced by the current round and tries to refute it.
Default posture is refute-unless-evidence-holds.

- **Internal hypotheses:** standard adversarial bar — look for a case the
  hypothesis doesn't explain, or an alternative explanation not yet ruled
  out.
- **External hypotheses:** held to a higher bar. Must show an exact version
  match (not "a version" — *this* version), a reproduction path that matches
  this codebase's actual call path (not just the same error type), and
  confirmation that the Internal Investigator found no plausible local cause.
  Default is refute even on a strong-looking symptom match.

Output: for each hypothesis, either "survived" (with what was checked and why
it held) or "refuted" (with the specific hole found — folded into the ruled-out
list so it's never retested).

### Fix-Implementer
Only invoked once a hypothesis survives the skeptic. Applies the minimal fix
on a branch, adds or updates a regression test derived from the repro case,
runs the full test suite, and reports: branch name, diff summary, test
added, suite result. **Never merges.** Never declares the bug fixed — that
determination belongs to the Verifier.

### Verifier
Independent from Fix-Implementer — never the agent that wrote the fix. Takes
the original repro case and runs it against the patched branch, actively
trying to show the bug still reproduces. Only after this check passes does
the pipeline report the bug as fixed. If verification isn't mechanically
possible (see Open Questions), the pipeline states that explicitly rather
than asserting success.

## Escalation Logic

If the skeptic refutes every hypothesis in a round, escalate: spawn parallel
investigators, each assigned a distinct alternate hypothesis (race condition,
data/state issue, config/env, etc.), explicitly informed by the ruled-out
list so escalation never retests a dead end. The External Researcher retries
with broadened search terms in the same round.

**Escalation cap:** default 2 escalation rounds beyond round 1 (tunable). If
nothing survives the skeptic after the cap is reached, stop auto-escalating
and produce a Decision Point instead of continuing indefinitely.

## Artifacts

### Ruled-Out List
Grows monotonically across the whole investigation. Each entry: the
hypothesis, the specific evidence that eliminated it, which agent/round
eliminated it. Visible to every subsequent investigator in the same run.

### Decision Point
Only produced if escalation hits its cap with nothing surviving. Contains:
the full ruled-out list, the strongest hypothesis that almost survived and
where it fell short, anything the External Researcher found even if it
didn't pass skepticism (a weak lead is still useful context), and an
explicit ask: keep digging, apply a workaround if one exists, or change
approach entirely. **No default action is taken** — this is a hard stop for
the user's judgment, consistent with how root `CLAUDE.md` already scopes
autonomy (strategic pivots need approval).

Persisted as a **GitHub issue**: milestone-less by default (it's an
investigation record, not a scheduled goal) and tagged with a `debugging`
label so it's distinguishable from goal-oriented-development's regular issue
queue. This reuses existing infrastructure rather than inventing a new file
convention, and gets a natural lifecycle for free — stays open while
unresolved, closes when eventually fixed, resumable by a future session
without re-deriving the ruled-out list from scratch.

Bugs resolved within the escalation budget produce **no persisted artifact**
beyond the final report — only the hard/unresolved cases leave a trace.

### Final Report
Written only after the Verifier's check completes (or, if verification
wasn't mechanically possible, states that explicitly). Includes the
ruled-out list as a record of what was checked.

## File Structure

Mirrors goal-oriented-development's layout:

```
.claude/skills/synapse/systematic-debugging/
├── SKILL.md
└── agents/
    ├── investigator.md
    ├── external-researcher.md
    ├── skeptic.md
    ├── fix-implementer.md
    └── verifier.md
```

## Testing / Validation Plan

goal-oriented-development was validated by running old-skill-vs-with-skill
comparisons on a real project (hotel-kline-game) and capturing transcripts —
that comparison, not abstract design review, is what built confidence in it.
Same approach here via skill-creator: run the full pipeline against a real
bug with some actual teeth (not a one-line typo), and compare the outcome
against how a normal conversational debugging session would have gone.

## Open Questions / Future Work

**Reproduction tiering.** Discussed at length: not every bug can produce an
automated repro. A three-tier model was proposed —

- Tier 1: automated repro (test/script) — Verifier re-runs it directly.
- Tier 2: live/manual repro (e.g. a Devvit playtest, browser interaction,
  deployed sandbox) — Investigator produces exact step-by-step instructions
  instead of a script; Verifier either drives them itself (if it has the
  right tooling, e.g. browser/computer-use access) or hands back a precise
  checklist rather than declaring victory unverified.
- Tier 3: no reliable repro obtainable — the pipeline never claims "fixed,"
  states plainly it couldn't mechanically re-verify, and asks the user to
  confirm in the field. Should also make the Skeptic more conservative
  earlier, since a hypothesis that can't be cheaply verified later deserves
  more scrutiny going in.

**V1 scope decision:** ship with Tier 1 only (automated repro required). The
user wants to think through how Tier 2/3 should actually work — mechanics,
tooling requirements, and whether the Skeptic's bar should shift — before
locking it in. This is a deliberate deferral, not an oversight: the rest of
the pipeline is fully specified and independently useful without it.

**Escalation cap value.** Defaulted to 2 rounds beyond round 1; may need
tuning once tested against a real hard bug.
