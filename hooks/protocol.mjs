import { readFileSync } from "node:fs";

export function readPayload() {
  try {
    return JSON.parse(readFileSync(0, "utf8"));
  } catch {
    return {};
  }
}

export function cwdOf(payload) {
  if (typeof payload.cwd === "string" && payload.cwd) return payload.cwd;
  const roots = payload.workspace_roots;
  if (Array.isArray(roots) && typeof roots[0] === "string" && roots[0]) {
    return roots[0];
  }
  return process.cwd();
}

export function sessionIdOf(payload) {
  return (
    payload.session_id ||
    payload.conversation_id ||
    payload.generation_id ||
    "unknown"
  );
}

export function eventNameOf(payload) {
  return String(payload.hook_event_name || payload.hookEventName || "");
}

export function briefOf(payload) {
  const fromTool = payload.tool_input;
  const candidates = [
    payload.task,
    payload.description,
    fromTool && fromTool.prompt,
    fromTool && fromTool.description,
  ];
  for (const value of candidates) {
    if (typeof value === "string" && value) return value;
  }
  return "";
}

export function commandOf(payload) {
  if (typeof payload.command === "string" && payload.command) {
    return payload.command;
  }
  const fromTool = payload.tool_input;
  if (fromTool && typeof fromTool.command === "string") return fromTool.command;
  return "";
}

export function emitContext(eventName, text) {
  process.stdout.write(
    JSON.stringify({
      additional_context: text,
      hookSpecificOutput: {
        hookEventName: eventName,
        additionalContext: text,
      },
    }),
  );
}

export function emitPermission(eventName, decision, reason) {
  const cursorDecision = decision === "ask" ? "deny" : decision;
  process.stdout.write(
    JSON.stringify({
      permission: cursorDecision,
      agent_message: reason,
      user_message: reason,
      hookSpecificOutput: {
        hookEventName: eventName,
        permissionDecision: decision,
        permissionDecisionReason: reason,
      },
    }),
  );
}
