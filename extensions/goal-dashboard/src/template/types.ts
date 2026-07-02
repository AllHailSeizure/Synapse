export interface ChecklistItem {
  text: string;
  checked: boolean;
}

export interface ParsedGoal {
  currentState: string;
  doneCriteria: string;
  constraints: string[];
  checklist: ChecklistItem[];
}

export type ParseResult = { ok: true; goal: ParsedGoal } | { ok: false; raw: string };
