import { describe, expect, it } from 'vitest';
import { parseIssueBody } from '../src/template/parser';

const WELL_FORMED = `## Current State
Nothing exists yet.

## Done Criteria
Users can log in with email and password.

## Constraints
- Use the existing auth module
- Do not add a new dependency

## Checklist
- [ ] Add login form
- [x] Add password hashing
`;

describe('parseIssueBody', () => {
  it('parses a well-formed goal-writer template', () => {
    const result = parseIssueBody(WELL_FORMED);

    expect(result.ok).toBe(true);
    if (!result.ok) return;

    expect(result.goal.currentState).toBe('Nothing exists yet.');
    expect(result.goal.doneCriteria).toBe('Users can log in with email and password.');
    expect(result.goal.constraints).toEqual(['Use the existing auth module', 'Do not add a new dependency']);
    expect(result.goal.checklist).toEqual([
      { text: 'Add login form', checked: false },
      { text: 'Add password hashing', checked: true },
    ]);
  });

  it('allows an empty Constraints section', () => {
    const body = `## Current State
State.

## Done Criteria
Criteria.

## Constraints

## Checklist
- [ ] Step one
`;
    const result = parseIssueBody(body);
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.goal.constraints).toEqual([]);
    }
  });

  it('falls back to raw when a required heading is missing', () => {
    const body = `## Current State
State.

## Done Criteria
Criteria.

## Checklist
- [ ] Step one
`;
    const result = parseIssueBody(body);
    expect(result).toEqual({ ok: false, raw: body });
  });

  it('falls back to raw when the checklist has no valid items', () => {
    const body = `## Current State
State.

## Done Criteria
Criteria.

## Constraints
- Some constraint

## Checklist
Nothing here matches the checkbox syntax.
`;
    const result = parseIssueBody(body);
    expect(result.ok).toBe(false);
  });

  it('falls back to raw for a body with no headings at all', () => {
    const body = 'Just some free text a human wrote directly on github.com.';
    const result = parseIssueBody(body);
    expect(result).toEqual({ ok: false, raw: body });
  });
});
