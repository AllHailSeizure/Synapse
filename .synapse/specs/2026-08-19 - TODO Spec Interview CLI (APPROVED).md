# 2026-08-19: TODO Spec Interview CLI (APPROVED)

## Intent

Synapse needs a script-first way to close product questions on specs without
keeping an agent in the chat loop for every answer. An agent drafts the
`PENDING` spec and the interview questions once; the operator runs a small
`TODO` CLI, sees open `SPEC:` rows, and answers in the terminal. Finishing
that interview is approval. The agent does not conduct the interview or invent
approval.

## Current context

- Specs already live under `.synapse/specs/` with synchronized filename and
  title status markers (`PENDING`, `APPROVED`, `IMPLEMENTED`, `CLOSED`), as
  defined in `skills/writing-specs/SKILL.md` and `AGENTS.md`.
- Spec drafting today is chat-shaped: `writing-specs` investigates, asks
  feature-defining questions in conversation, then asks for overall approval
  in chat. There is no machine-readable question file and no terminal interview.
- Interactive CLI precedent exists in `apps/weedeat/` (`cli.py`, `console.py`):
  survey → interactive prompt when stdin/stdout are TTYs.
- Codex-style agent registrations already live under `.codex/agents/synapse/`
  (e.g. goal-writer). A dedicated spec-writer can follow that pattern; Claude
  adapters under `agents/` are optional parity later.
- This v1 does not depend on `writing-plans`, goal-issue list rows, or bandaid
  automations.

## Expected behavior

### Actors

- **Operator** — human who names a feature to specify, then later answers the
  interview in a terminal.
- **Spec-writer agent** — one bounded agent call that grounds and drafts. Owns
  repository investigation, the `PENDING` spec body, and the sibling questions
  file. Does not approve. Does not run the interview.
- **CLI (`TODO`)** — script only. Owns listing, interview, appending answers,
  and status rename. No model calls during list or interview.

### Spec-writer (agent)

Triggered when the operator asks to write/capture a spec for a named feature
(or issue), via the Synapse spec-writer entrypoint (skill and/or registered
agent) — not by selecting a `SPEC:` row in `TODO`.

The agent:

1. Grounds in the repo the same way `writing-specs` requires (current behavior,
   files/modules by path, scope, non-goals, success criteria).
2. Writes a `PENDING` spec under `.synapse/specs/` using the existing naming
   and title conventions.
3. Writes a sibling machine-readable questions file tied to that spec.
4. Puts only **feature-defining** gaps in that file (evidence-answerable and
   reversible technical choices are resolved in the draft, not asked).
5. Ensures the interview will have a required **closer** (is this what you
   want / any remarks). If there are no feature-defining gaps, the questions
   file may be empty or omit items — the CLI still supplies the closer.
6. Stops. It does not wait in chat to collect answers, does not flip status to
   `APPROVED`, and does not start a plan or implementation.

**Second agent call (optional, rare):** only if the draft cannot be written
without an answer the questions file cannot express, or a later operator remark
forces a product fork that needs a rewrite. Normal path is one draft call, then
CLI interview only.

### Inventory (CLI)

Running `TODO` in a repository (git root discovery like weedeat):

1. Scans `.synapse/specs/` for specs whose status is `PENDING`.
2. Lists one row per such spec, prefixed `SPEC:`, with a short label from the
   filename/title.
3. Does not list `APPROVED`, `IMPLEMENTED`, or `CLOSED` specs.
4. If none are pending, shows a clear empty state and exits successfully.

### Selection (CLI)

- Operator selects one `SPEC:` row.
- Selection always starts the interview. No separate approve command; no
  submenu in v1. Selection does not spawn the spec-writer.

### Interview (CLI)

- Questions come from the sibling questions file. The CLI never invents
  product questions beyond the required closer.
- Every interview includes the closer (accept / remarks, remarks may be
  “none”).
- If the questions file is missing or has zero feature items, interview is
  closer-only. `PENDING` means a human question is open.
- Present each question in the terminal (prompt, options, recommendation when
  provided). Collect answers without an agent.
- Non-interactive stdin/stdout: do not interview; error (or list-only dry-run)
  and leave status unchanged.

### Completion = approval (CLI)

When the operator finishes the interview:

1. Append answers to the spec in a durable readable section, including remarks
   or “none”.
2. Rename `PENDING` → `APPROVED` in filename and title (same rules as
   `writing-specs`).
3. That completion is approval.

Abort mid-interview: leave `PENDING`; do not approve. Partial save of answers
is an implementation detail; approval requires the closer.

### Failure / empty cases

- Missing `.synapse/specs/`: empty inventory.
- Spec-writer cannot ground or define the feature: it stops without writing a
  false `APPROVED` artifact; operator gets a clear failure/stop reason.
- Corrupt questions file: CLI refuses interview for that row; status unchanged.
- Spec vanishes between list and select: error; status unchanged.

## Scope

**In v1**

- Spec-writer agent/skill that produces `PENDING` spec + sibling questions file
  (closer always applicable via CLI).
- `TODO` inventory of `PENDING` specs as `SPEC:` rows.
- Terminal interview; append answers; rename to `APPROVED` on completion.
- Hard split: agent drafts; script interviews and approves.

**Non-goals (expand later)**

- `ISSUE:` rows or spawning the spec-writer from the `TODO` list.
- `PLAN:` rung or plan writing.
- Launching implementation / code agents.
- Auto-chore / blocked `CHORE:` rows.
- Full rewrite of chat-only flows in `writing-specs` beyond what’s needed so
  the agent emits the questions file and stops before chat approval (skill
  catch-up may be part of shipping this feature).
- Multi-select or batch non-interactive approve.

## Decisions

- **v1 is specs-only, but includes both halves** — agent draft + CLI interview.
- **`PENDING` means an open human question** — at minimum the closer.
- **Finishing the interview creates `APPROVED`** — no second approval step.
- **No agent during interview** — token cost and authority stay with the
  operator after the draft.
- **Spec-writer is not launched from `SPEC:` selection** — selection means
  interview; drafting is a separate operator-triggered entrypoint.
- **Plan and chores stay out** until a later expansion.

## Success criteria

- Operator can invoke the spec-writer for a named feature and get a `PENDING`
  spec under `.synapse/specs/` plus a sibling questions file (possibly empty
  of feature items).
- That agent call does not mark the spec `APPROVED` and does not run a chat
  interview to collect answers.
- `TODO` lists the new spec as `SPEC: …`.
- Selecting it runs a terminal interview that includes the closer.
- Completing the interview appends answers and renames to `APPROVED` in
  filename and title.
- Aborting leaves `PENDING`.
- `APPROVED` / `IMPLEMENTED` / `CLOSED` specs do not appear in the list.
- No model is invoked by the CLI during list or interview.
- Empty pending set yields a clear empty state.
