#!/usr/bin/env node
// UserPromptSubmit hook: re-asserts the scope boundary every turn on hosts
// that inject additionalContext here (Codex). Cursor gets the same
// text from session-briefing instead.
//
// Fails silent: any problem here means no injection, never a per-turn error.

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { emitContext } from "./protocol.mjs";

const MAX_CHARS = 2000;

try {
  const here = dirname(fileURLToPath(import.meta.url));
  const raw = readFileSync(join(here, "scope-reminder.md"), "utf8");
  const reminder = raw.trim();
  if (reminder) emitContext("UserPromptSubmit", reminder.slice(0, MAX_CHARS));
} catch {
  // Unreadable file, bad encoding, anything else -- stay quiet.
}

process.exit(0);
