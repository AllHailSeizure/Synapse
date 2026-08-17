---
name: writing-specs
description: >-
  Capture feature intent in a concise, approved specification document. Use
  when the user explicitly asks to write, capture, or document a feature spec,
  whether the intent comes from thinking, a selected issue, or an existing
  discussion. Do not trigger automatically after thinking, use for broad
  exploratory conversation, implement the feature, or write an implementation
  plan.
---

# Writing Specs

Produce one reviewable document that defines what a feature means without
dictating how to implement it.

## Input and output

Input is one feature idea or selected feature issue plus any conversation,
notes, or decisions the user wants captured. Output is one specification whose
product meaning the user can approve.

The human owns purpose, user-visible behavior, experience, scope, exclusions,
and meaningful product tradeoffs. The agent owns repository investigation,
reversible technical choices, and later implementation mechanics.

## Process

### 1. Establish the feature boundary

Collect the source intent from the conversation, issue, and supplied notes.
Restate the desired outcome in one sentence. Preserve decisions already made;
do not reopen them without contradictory evidence.

If the request contains independent features that cannot share one coherent
success condition, list the split and ask which feature to specify first. Do
not hide multiple deliverables inside one spec.

### 2. Inspect the existing product

Read the relevant code, tests, documentation, selected issue and milestone,
and recent history. Determine:

- the current user-visible behavior;
- the flow, interface, or subsystem the feature affects;
- the specific files, modules, or interfaces the feature will touch, by path;
- repository constraints or conventions that affect the feature boundary;
- claims in the source intent that the current product contradicts.

Investigate only the context needed to define this feature. Do not design the
implementation plan. The goal is not to plan the implementation but to ground
the spec in the real code, so step 6 can point at what exists instead of
describing it in the abstract.

### 3. Build a decision inventory

Classify every uncertainty that would affect the spec:

- **Evidence-answerable** — resolve it from the repository or authoritative
  source.
- **Reversible technical** — choose it using project conventions; normally
  omit it from the spec.
- **Feature-defining** — ask the human when the source permits materially
  different interpretations of the requested outcome and implementation
  cannot preserve intent without choosing one.
- **Out of scope** — record it as a non-goal when an implementer might
  otherwise reasonably include it.
- **Blocking** — a dependency this spec cannot resolve on its own: another
  spec under `.synapse/specs/` that isn't yet `APPROVED`, code the feature
  needs that doesn't exist yet, or an external decision recorded elsewhere.
  Record it as a blocker rather than guessing to fill the gap.

Do not inventory every conceivable decision. Omit optional embellishments,
speculative extensions, and future possibilities that are not required to
define the requested feature.

File placement, internal types, algorithms, and code structure are normally
technical. Actors, permissions, triggers, visible results, failure behavior,
and product boundaries are normally feature-defining.

### 4. Resolve feature-defining decisions

Resolve evidence and technical questions without involving the user. For each
remaining feature-defining question, present:

1. the decision;
2. why it changes the feature;
3. viable options and their tradeoffs, when alternatives are real;
4. a recommendation;
5. the focused question the user must answer.

Group up to three independent decisions. Ask sequentially when one answer
changes the next decision. Update the inventory after each response.

If fundamental intent still needs open-ended exploration, stop drafting and
return to `thinking`. Resume this process when the user asks to capture the
result. Begin drafting only when no unresolved feature-defining decision would
force an implementer to invent product behavior.

### 5. Create the pending document

Store every specification under `./.synapse/specs/` from the repository root.
Create the directory when it does not exist.

Use these names:

- Issue-backed filename: `YYYY-MM-DD - Issue 103 (PENDING).md`
- Other filename: `YYYY-MM-DD - Short Feature Name (PENDING).md`
- Issue-backed title: `# YYYY-MM-DD: Issue 103 (PENDING)`
- Other title: `# YYYY-MM-DD: Short Feature Name (PENDING)`

When the spec is `BLOCKED`, append that marker after the status in both
filename and title, e.g. `YYYY-MM-DD - Issue 103 (APPROVED) (BLOCKED).md` and
`# YYYY-MM-DD: Issue 103 (APPROVED) (BLOCKED)`. See Status lifecycle for what
`BLOCKED` requires.

Use the creation date and preserve it through later status changes. Sanitize
feature names for the filesystem. The title may use a colon; the filename must
use a hyphen because Windows filenames cannot contain colons. Do not commit
automatically.

### 6. Write the specification

Cover each topic below, combining headings when the feature is small:

- **References** — the GitHub issue(s) this spec is based on, if any, and any
  other specs under `.synapse/specs/` this one depends on. Link dependency
  specs by filename so a reader can open them directly.
- **Intent** — who needs the feature, the problem, and the desired outcome.
- **Current context** — only existing behavior and constraints that affect the
  feature, grounded in the actual code: name the files, modules, or
  interfaces involved by path rather than describing them abstractly.
- **Expected behavior** — actors, triggers, main flow, visible results, and
  relevant failure or empty states, tied to the concrete code surfaces from
  Current context where relevant.
- **Scope** — what is included, important boundaries, and explicit non-goals.
- **Decisions** — consequential choices made and why; omit routine technical
  mechanics.
- **Blockers** — only when the spec is `BLOCKED`: exactly what blocks it and
  which file that blocker lives in (a dependency spec's filename, an issue
  number, or the code path that doesn't exist yet). Omit this section
  entirely when nothing blocks the spec.
- **Success criteria** — observable conditions that show the intended feature
  exists and behaves correctly.

Write requirements precisely enough that two reasonable implementers would
not produce materially different user-visible behavior, and precisely enough
about the code it touches that implementing it does not require an
exploratory agent to first go find the relevant files. This is distinct from
prescribing the implementation: pointing at what exists is required, but
architecture, algorithms, sequencing, and test commands for what doesn't yet
exist stay later technical work unless one is itself a product constraint.

### 7. Self-review the document

Read the complete document once and apply every check:

- **Source fidelity:** Does it preserve the supplied intent and settled
  decisions?
- **Completeness:** Are actors, triggers, outcomes, boundaries, and relevant
  failures defined?
- **Ambiguity:** Could two reasonable readings create materially different
  features?
- **Pressure:** Under the single most plausible invalid, empty, unavailable,
  or impossible state, do requirements conflict or force an implementer to
  invent user-visible behavior? Resolve that state; do not enumerate remote
  edge cases.
- **Consistency:** Do sections or success criteria contradict one another?
- **Scope:** Did the draft add attractive but unauthorized behavior?
- **Technical freedom:** Did it prescribe implementation without a product
  reason?
- **Groundedness:** Does the spec name the actual files, modules, or
  interfaces involved, or would an implementer need an exploratory pass to
  locate them first?
- **Provenance:** Is the source issue referenced, if one exists, along with
  any specs this one depends on?
- **Blocker clarity:** If the spec is `BLOCKED`, does it name the specific
  blocker and the file it lives in, rather than a bare marker?
- **Reviewability:** Are there placeholders, hidden open product questions, or
  success criteria that cannot be observed?

Fix evidence-answerable and technical defects directly. Return to step 4 when
a correction requires product authority.

### 8. Deliver for approval

Tell the user the document path and summarize the feature-defining decisions
captured. Ask for one overall judgment: whether the document adequately states
the feature.

If the user changes the meaning, keep or return the status to `PENDING`, edit
the document, and repeat step 7. When the user explicitly approves it, change
the title status to `APPROVED` and rename the file to match.

Approval permits later technical work within the spec; it does not authorize
implementation in this workflow. Stop after approval. Do not commit,
transition into `writing-plans`, or implement unless the user separately asks.

## Status lifecycle

Keep the filename and document title synchronized:

- `PENDING` — the spec is being drafted, has unresolved feature meaning, or
  has changed since its last approval.
- `APPROVED` — the user has approved the current document as an adequate
  statement of the feature.
- `IMPLEMENTED` — implementation governed by the approved spec has completed
  and its success criteria have been verified.

`BLOCKED` is an additional marker, not a replacement status: append it after
`PENDING` or `APPROVED` when something outside this spec's control prevents
it from moving forward, e.g. `(APPROVED) (BLOCKED)`. A spec cannot be
`IMPLEMENTED` and `BLOCKED` at once. Every `BLOCKED` spec must state, in its
Blockers section, exactly what blocks it and which file that blocker lives
in — another spec's filename, an issue number, or the code path that doesn't
exist yet; a bare `(BLOCKED)` with no named cause is not a valid state. Drop
the marker as soon as the named blocker clears rather than leaving it stale.

`writing-specs` owns `PENDING → APPROVED` and applying or clearing `BLOCKED`.
The later implementation workflow owns `APPROVED → IMPLEMENTED`; it must not
make that transition for partial or unverified work, or for a spec still
marked `BLOCKED`. Preserve the date and issue or feature identifier when
renaming.
