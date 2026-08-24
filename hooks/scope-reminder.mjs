#!/usr/bin/env node
// UserPromptSubmit hook: re-asserts the scope boundary every turn.
//
// Same rationale as succinct-reminder.mjs: a CLAUDE.md rule decays as the
// conversation grows. This lands at the end of context immediately before
// the response, every turn, so it can't get buried under skill instructions
// and tool output the way a SessionStart-only injection would.
//
// Fails silent: any problem here means no injection, never a per-turn error.

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_CHARS = 2000;

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
  const raw = readFileSync(join(here, "scope-reminder.md"), "utf8");
  const reminder = raw.trim();

  if (reminder) emit(reminder.slice(0, MAX_CHARS));
} catch {
  // Unreadable file, bad encoding, anything else -- stay quiet.
}

process.exit(0);
