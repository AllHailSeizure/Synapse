#!/usr/bin/env node
// Gate on shell: deny unrequested broad verification runs.
//
// Codex: PreToolUse Bash. Cursor: beforeShellExecution.
//
// Fires only where a repo has opted in via .synapse/verification-budget.json
// ({ broad: [...], scoped: [...] }). No config means no gate.
//
// Fails open. Any error here allows the command.

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import {
  commandOf,
  cwdOf,
  emitPermission,
  readPayload,
} from "./protocol.mjs";

function loadConfig(cwd) {
  const path = join(cwd, ".synapse", "verification-budget.json");
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

function main() {
  const payload = readPayload();
  const command = commandOf(payload);
  if (!command) process.exit(0);

  const cfg = loadConfig(cwdOf(payload));
  if (!cfg) process.exit(0);

  if (matchesAny(command, cfg.scoped)) process.exit(0);

  if (matchesAny(command, cfg.broad)) {
    emitPermission(
      "PreToolUse",
      "deny",
      cfg.reason ||
        "Synapse verification-budget gate: this reads as a full verification run, not a targeted " +
          "debug run. The user runs these themselves and CI covers the rest. Scope the command to " +
          "one file/test if you're actually debugging, or stop and continue the assigned task.",
    );
    process.exit(0);
  }

  process.exit(0);
}

try {
  main();
} catch {
  process.exit(0);
}
