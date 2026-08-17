#!/usr/bin/env node
// SessionStart hook: injects the Synapse operating briefing into every session,
// plus which of the target repo's .synapse/ files actually exist.

import { readFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const BRIEFING = join(HERE, "synapse-briefing.md");

const SYNAPSE_FILES = [
  ".synapse/identity.md",
  ".synapse/verification.md",
  ".synapse/bandaids.md",
  ".synapse/weedeat.md",
];

const SYNAPSE_DIRS = [".synapse/specs", ".synapse/plans"];

function readStdin() {
  try {
    return readFileSync(0, "utf8");
  } catch {
    return "";
  }
}

function resolveCwd() {
  try {
    const payload = JSON.parse(readStdin());
    if (typeof payload.cwd === "string" && payload.cwd) return payload.cwd;
  } catch {
    // Hook payload is optional; fall back to the process working directory.
  }
  return process.cwd();
}

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

const briefing = readFileSync(BRIEFING, "utf8").trimEnd();
const context = `${briefing}\n\n## This repo\n\n${repoStatus(resolveCwd())}\n`;

process.stdout.write(
  JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: context,
    },
  }),
);
