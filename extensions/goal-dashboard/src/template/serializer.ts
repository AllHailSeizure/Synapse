import { ParsedGoal } from './types';

// Literal inverse of parseIssueBody for the structured case:
// parseIssueBody(serializeGoal(goal)) must round-trip to an equal ParsedGoal.
export function serializeGoal(goal: ParsedGoal): string {
  const constraintsBlock = goal.constraints.map((c) => `- ${c}`).join('\n');
  const checklistBlock = goal.checklist
    .map((item) => `- [${item.checked ? 'x' : ' '}] ${item.text}`)
    .join('\n');

  return [
    '## Current State',
    goal.currentState,
    '',
    '## Done Criteria',
    goal.doneCriteria,
    '',
    '## Constraints',
    constraintsBlock,
    '',
    '## Checklist',
    checklistBlock,
  ].join('\n');
}
