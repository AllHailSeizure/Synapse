#!/usr/bin/env node
// PreToolUse/PostToolUse gate on subagent launches.
//
// Enforces the mechanical rules from the 2026-08-20 fan-out retrospective
// (.synapse/retrospectives/): bounded concurrency, task packets instead of
// forwarded session history, and a human checkpoint between waves.
//
// Fails open. Any error here allows the spawn.

import {
  readFileSync,
  mkdirSync,
  readdirSync,
  writeFileSync,
  appendFileSync,
  rmSync,
  statSync,
  existsSync,
} from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { createHash } from "node:crypto";

const DEFAULTS = {
  maxConcurrent: 2,
  maxPromptChars: 12000,
  waveSize: 6,
  staleMinutes: 90,
};

function readStdin() {
  try {
    return JSON.parse(readFileSync(0, "utf8"));
  } catch {
    return {};
  }
}

function loadConfig(cwd) {
  const path = join(cwd || process.cwd(), ".synapse", "fanout.json");
  if (!existsSync(path)) return DEFAULTS;
  try {
    return { ...DEFAULTS, ...JSON.parse(readFileSync(path, "utf8")) };
  } catch {
    return DEFAULTS;
  }
}

function stateDir(sessionId) {
  const safe = String(sessionId || "unknown").replace(/[^A-Za-z0-9_-]/g, "_");
  const dir = join(homedir(), ".claude", "synapse", "fanout", safe);
  mkdirSync(dir, { recursive: true });
  return dir;
}

function briefHash(prompt) {
  return createHash("sha1").update(prompt).digest("hex").slice(0, 12);
}

function activeMarkers(dir, staleMinutes) {
  const cutoff = Date.now() - staleMinutes * 60 * 1000;
  const live = [];
  for (const name of readdirSync(dir)) {
    if (!name.endsWith(".lane")) continue;
    const path = join(dir, name);
    try {
      if (statSync(path).mtimeMs < cutoff) rmSync(path, { force: true });
      else live.push(name);
    } catch {
      // Racing sibling launch already cleaned it up.
    }
  }
  return live;
}

function spawnsThisSession(dir) {
  const log = join(dir, "total.log");
  if (!existsSync(log)) return 0;
  try {
    return readFileSync(log, "utf8").split("\n").filter(Boolean).length;
  } catch {
    return 0;
  }
}

function decide(decision, reason) {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: decision,
        permissionDecisionReason: reason,
      },
    })
  );
  process.exit(0);
}

function main() {
  const payload = readStdin();
  const prompt = payload?.tool_input?.prompt;
  if (typeof prompt !== "string") process.exit(0);

  const cfg = loadConfig(payload.cwd);
  const dir = stateDir(payload.session_id);
  const hash = briefHash(prompt);

  if (payload.hook_event_name === "PostToolUse") {
    for (const name of readdirSync(dir)) {
      if (name.startsWith(`${hash}-`) && name.endsWith(".lane")) {
        rmSync(join(dir, name), { force: true });
        break;
      }
    }
    process.exit(0);
  }

  const active = activeMarkers(dir, cfg.staleMinutes);
  const total = spawnsThisSession(dir);
  const label = payload?.tool_input?.description || payload?.tool_input?.subagent_type || "this agent";

  if (prompt.length > cfg.maxPromptChars) {
    decide(
      "deny",
      `Synapse fan-out gate: the brief for "${label}" is ${prompt.length} chars (cap ${cfg.maxPromptChars}). ` +
        `A brief that long means session history is being forwarded — the failure that consumed a full weekly allowance on 2026-08-20. ` +
        `Send a task packet instead: the one task's text, its base commit or branch, allowed files, the done condition, one focused verify command, ` +
        `and the rule that adjacent findings get recorded rather than chased. Long material goes in a file; pass the path.`
    );
  }

  if (active.length >= cfg.maxConcurrent) {
    decide(
      "deny",
      `Synapse fan-out gate: ${active.length} subagent lane(s) already open (cap ${cfg.maxConcurrent}). ` +
        `Close the current wave before opening another — each task published and CI green, explicitly deferred with a blocker, or stopped with a clean handoff. ` +
        `Independent reviewer lanes wait until the implementation slots are idle.`
    );
  }

  appendFileSync(join(dir, "total.log"), `${new Date().toISOString()} ${hash}\n`);

  if (total > 0 && total % cfg.waveSize === 0) {
    decide(
      "ask",
      `Synapse fan-out gate: wave checkpoint — ${total} subagent launches so far this session, and "${label}" starts another. ` +
        `Before approving, expect a report of completed tasks, published PRs, remaining plan tasks, and whether this lane adds a new worktree, import, or full-CI cycle.`
    );
  }

  writeFileSync(join(dir, `${hash}-${process.pid}-${total}.lane`), label);
  process.exit(0);
}

try {
  main();
} catch {
  process.exit(0);
}
