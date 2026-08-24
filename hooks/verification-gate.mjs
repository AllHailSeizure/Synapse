#!/usr/bin/env node
// PreToolUse gate on Bash: deny unrequested broad verification runs.
//
// Prompted by a 2026-08-24 incident (.synapse/retrospectives/): a session ran
// a project's full GUT suite three times unprompted, on top of fixing a bug
// the user had deliberately deferred, and burned a full session's budget on
// self-directed prep before touching the assigned task.
//
// What counts as "the full suite" vs. "a targeted debug run" is project-
// specific, so this only fires where a repo has opted in via
// .synapse/verification-budget.json ({ broad: [...], scoped: [...] }, both
// regex or substring). No config in the repo means no gate at all.
//
// Fails open. Any error here allows the command.

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

function readStdin() {
  try {
    return JSON.parse(readFileSync(0, "utf8"));
  } catch {
    return {};
  }
}

function loadConfig(cwd) {
  const path = join(cwd || process.cwd(), ".synapse", "verification-budget.json");
  if (!existsSync(path)) return null;
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch {
    return null;
  }
}

function matchesAny(command, patterns) {
  return (patterns || []).some((p) => {
    try {
      return new RegExp(p).test(command);
    } catch {
      return command.includes(p);
    }
  });
}

function deny(reason) {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: reason,
      },
    })
  );
  process.exit(0);
}

function main() {
  const payload = readStdin();
  const command = payload?.tool_input?.command;
  if (typeof command !== "string") process.exit(0);

  const cfg = loadConfig(payload.cwd);
  if (!cfg) process.exit(0);

  if (matchesAny(command, cfg.scoped)) process.exit(0);

  if (matchesAny(command, cfg.broad)) {
    deny(
      cfg.reason ||
        "Synapse verification-budget gate: this reads as a full verification run, not a targeted " +
          "debug run. The user runs these themselves and CI covers the rest. Scope the command to " +
          "one file/test if you're actually debugging, or stop and continue the assigned task."
    );
  }

  process.exit(0);
}

try {
  main();
} catch {
  process.exit(0);
}
