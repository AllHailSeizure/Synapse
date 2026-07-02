import { ChecklistItem, ParsedGoal, ParseResult } from './types';

// goal-writer's "## Issue Title" heading maps to the GitHub issue's native
// title field, not the body, so it's not part of what this parser looks for.
const REQUIRED_HEADINGS = ['Current State', 'Done Criteria', 'Constraints', 'Checklist'] as const;

const CHECKLIST_LINE = /^-\s\[([ xX])\]\s+(.+)$/;

function extractSections(body: string): Map<string, string> {
  const sections = new Map<string, string>();
  let currentHeading: string | null = null;
  let buffer: string[] = [];

  const flush = () => {
    if (currentHeading !== null) {
      sections.set(currentHeading, buffer.join('\n').trim());
    }
  };

  for (const line of body.split('\n')) {
    const headingMatch = /^##\s+(.+)$/.exec(line);
    if (headingMatch) {
      flush();
      currentHeading = headingMatch[1].trim();
      buffer = [];
    } else {
      buffer.push(line);
    }
  }
  flush();

  return sections;
}

function parseConstraints(text: string): string[] {
  return text
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('- '))
    .map((line) => line.slice(2).trim());
}

function parseChecklist(text: string): ChecklistItem[] {
  return text
    .split('\n')
    .map((line) => line.trim())
    .map((line) => CHECKLIST_LINE.exec(line))
    .filter((match): match is RegExpExecArray => match !== null)
    .map((match) => ({ checked: match[1].toLowerCase() === 'x', text: match[2].trim() }));
}

// Binary by design: either the body matches the goal-writer template well
// enough to edit as structured fields, or the caller falls back to raw-text
// editing. No partial-field mixed mode.
export function parseIssueBody(body: string): ParseResult {
  const sections = extractSections(body);

  for (const heading of REQUIRED_HEADINGS) {
    if (!sections.has(heading)) {
      return { ok: false, raw: body };
    }
  }

  const checklist = parseChecklist(sections.get('Checklist')!);
  if (checklist.length === 0) {
    return { ok: false, raw: body };
  }

  const goal: ParsedGoal = {
    currentState: sections.get('Current State')!,
    doneCriteria: sections.get('Done Criteria')!,
    constraints: parseConstraints(sections.get('Constraints')!),
    checklist,
  };

  return { ok: true, goal };
}
