#!/usr/bin/env node
// UserPromptSubmit hook: re-asserts the Succinct response rules every turn.
//
// Output styles are the only lever that edits the system prompt, and Claude
// Desktop does not expose them. A SessionStart injection decays as the
// conversation grows; this lands at the end of context immediately before the
// response, which is the closest available equivalent.
//
// This runs on EVERY prompt, so it fails silent rather than loud: any problem
// means no injection, never a per-turn error in the user's face. Every
// injection also persists in the transcript, so cost is (length x turns) --
// hence MAX_CHARS.

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_CHARS = 4000;

function emit(context) {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "UserPromptSubmit",
        additionalContext: context,
      },
    }),
  );
}

try {
  const here = dirname(fileURLToPath(import.meta.url));
  const raw = readFileSync(join(here, "succinct-reminder.md"), "utf8");
  const reminder = raw.trim();

  // An empty or missing reminder is a no-op, not an error: injecting nothing
  // is always safer than interrupting the turn.
  if (reminder) emit(reminder.slice(0, MAX_CHARS));
} catch {
  // Unreadable file, bad encoding, anything else -- stay quiet and let the
  // turn proceed without the reminder.
}

process.exit(0);
