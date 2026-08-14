---
name: writing-specs
description: >-
  Capture feature intent in a concise, approved specification document. Use
  when the user explicitly asks to write, capture, or document a feature spec,
  whether the intent comes from thinking, a selected issue, or an existing
  discussion. Always run the thinking skill first to establish shared,
  plain-language understanding before writing. Do not trigger automatically
  after thinking, implement the feature, or write an implementation plan.
---

# Writing Specs

Produce one reviewable document that defines what a feature means without
dictating how to implement it.

## Mandatory thinking handoff

Invoke `thinking` before drafting, creating a file, or inventorying product
decisions. Do not satisfy this instruction by merely reading the thinking
skill, reasoning privately, or announcing that intent matters. Run its
conversational process with the user.

Use thinking to establish, in plain language:

- what the issue or feature is;
- why it matters;
- what currently happens;
- what the user is trying to change;
- which parts remain genuinely unsettled.

Let repository evidence ground that conversation, but translate technical
facts into effects the user can recognize. Do not make code structure or the
issue's existing vocabulary the premise of questions the user must answer.

Stay in thinking until the user can recognize and correct the working
understanding. If the feature was already clear, this may be one brief
synthesis and an opportunity to correct it; do not manufacture an interview.
An explicit request to write a spec counts as the requested capture once that
understanding settles. Only then begin the document workflow.

## Input and output

Input is one feature idea or selected feature issue plus any conversation,
notes, or decisions the user wants captured. Output is one specification whose
product meaning the user can approve.

The human owns purpose, user-visible behavior, experience, scope, exclusions,
and meaningful product tradeoffs. The agent owns repository investigation,
reversible technical choices, and later implementation mechanics.

## Process

### 1. Receive the thinking synthesis

Carry forward the plain-language understanding, settled decisions, remaining
questions, and relevant evidence developed through `thinking`. Restate the
desired outcome in one sentence. Preserve decisions already made; do not
reopen them without contradictory evidence.

If the request contains independent features that cannot share one coherent
success condition, list the split and ask which feature to specify first. Do
not hide multiple deliverables inside one spec.

### 2. Inspect the existing product

Read the relevant code, tests, documentation, selected issue and milestone,
and recent history. Determine:

- the current user-visible behavior;
- the flow, interface, or subsystem the feature affects;
- repository constraints or conventions that affect the feature boundary;
- claims in the source intent that the current product contradicts.

Investigate only the context needed to define this feature. Do not design the
implementation plan.

### 3. Build a decision inventory

Classify every uncertainty that would affect the spec:

- **Evidence-answerable** — resolve it from the repository or authoritative
  source.
- **Reversible technical** — choose it using project conventions; normally
  omit it from the spec.
- **Feature-defining** — ask the human because it changes user-visible
  behavior, experience, scope, exclusions, or a meaningful product tradeoff.
- **Out of scope** — record it as a non-goal when an implementer might
  otherwise reasonably include it.

File placement, internal types, algorithms, and code structure are normally
technical. Actors, permissions, triggers, visible results, failure behavior,
and product boundaries are normally feature-defining.

### 4. Return feature-defining decisions to thinking

Resolve evidence and technical questions without involving the user. When a
feature-defining question remains, resume `thinking`; do not turn this step
into a requirements interview owned by `writing-specs`.

Explain the affected part of the feature in ordinary language before asking
for a decision. Explore the user's problem and observable consequences, then
carry the resulting synthesis back into the decision inventory.

Begin drafting only when thinking has resolved enough feature meaning that an
implementer would not be forced to invent product behavior.

### 5. Create the pending document

Store every specification under `./synapse/specs/` from the repository root.
Create the directory when it does not exist.

Use these names:

- Issue-backed filename: `YYYY-MM-DD - Issue 103 (PENDING).md`
- Other filename: `YYYY-MM-DD - Short Feature Name (PENDING).md`
- Issue-backed title: `# YYYY-MM-DD: Issue 103 (PENDING)`
- Other title: `# YYYY-MM-DD: Short Feature Name (PENDING)`

Use the creation date and preserve it through later status changes. Sanitize
feature names for the filesystem. The title may use a colon; the filename must
use a hyphen because Windows filenames cannot contain colons. Do not commit
automatically.

### 6. Write the specification

Cover each topic below, combining headings when the feature is small:

- **Intent** — who needs the feature, the problem, and the desired outcome.
- **Current context** — only existing behavior and constraints that affect the
  feature.
- **Expected behavior** — actors, triggers, main flow, visible results, and
  relevant failure or empty states.
- **Scope** — what is included, important boundaries, and explicit non-goals.
- **Decisions** — consequential choices made and why; omit routine technical
  mechanics.
- **Success criteria** — observable conditions that show the intended feature
  exists and behaves correctly.

Write requirements precisely enough that two reasonable implementers would
not produce materially different user-visible behavior. Leave architecture,
files, algorithms, sequencing, and test commands to later technical work unless
one is itself a product constraint.

### 7. Self-review the document

Read the complete document once and apply every check:

- **Source fidelity:** Does it preserve the supplied intent and settled
  decisions?
- **Completeness:** Are actors, triggers, outcomes, boundaries, and relevant
  failures defined?
- **Ambiguity:** Could two reasonable readings create materially different
  features?
- **Consistency:** Do sections or success criteria contradict one another?
- **Scope:** Did the draft add attractive but unauthorized behavior?
- **Technical freedom:** Did it prescribe implementation without a product
  reason?
- **Reviewability:** Are there placeholders, hidden open product questions, or
  success criteria that cannot be observed?

Fix evidence-answerable and technical defects directly. Return to step 4 and
resume `thinking` when a correction requires product authority.

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

`writing-specs` owns `PENDING → APPROVED`. The later implementation workflow
owns `APPROVED → IMPLEMENTED`; it must not make that transition for partial or
unverified work. Preserve the date and issue or feature identifier when
renaming.
