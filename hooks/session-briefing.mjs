#!/usr/bin/env node
// SessionStart hook: injects the Synapse operating briefing into every session,
// plus which of the target repo's .synapse/ files actually exist.
// Cursor cannot re-inject per turn, so the scope reminder is appended here too.

import { readFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { cwdOf, emitContext, readPayload } from "./protocol.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const BRIEFING = join(HERE, "synapse-briefing.md");
const SCOPE = join(HERE, "scope-reminder.md");

const SYNAPSE_FILES = [
  ".synapse/identity.md",
  ".synapse/verification.md",
  ".synapse/bandaids.md",
  ".synapse/weedeat.md",
];

const SYNAPSE_DIRS = [".synapse/specs", ".synapse/plans"];

function repoStatus(cwd) {
  const present = [...SYNAPSE_FILES, ...SYNAPSE_DIRS].filter((entry) =>
    existsSync(join(cwd, entry)),
  );

  if (!existsSync(join(cwd, ".synapse"))) {
    return "This repo has no `.synapse/` directory. Skills fall back to their documented defaults — do not stop, and do not create the directory unprompted.";
  }

  if (present.length === 0) {
    return "This repo has a `.synapse/` directory but none of the known configuration files. Skills fall back to their documented defaults.";
  }

  return `This repo's \`.synapse/\` contains: ${present.join(", ")}. Read a file only when the skill you are running calls for it.`;
}

const payload = readPayload();
const briefing = readFileSync(BRIEFING, "utf8").trimEnd();
let scope = "";
try {
  scope = readFileSync(SCOPE, "utf8").trim();
} catch {
  // Scope file missing is not a reason to skip the briefing.
}

const parts = [
  briefing,
  `## This repo\n\n${repoStatus(cwdOf(payload))}`,
];
if (scope) parts.push(`## Scope\n\n${scope}`);

emitContext("SessionStart", `${parts.join("\n\n")}\n`);
