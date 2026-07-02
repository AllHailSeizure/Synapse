import { describe, expect, it } from 'vitest';
import { parseIssueBody } from '../src/template/parser';
import { serializeGoal } from '../src/template/serializer';
import { ParsedGoal } from '../src/template/types';

describe('serializeGoal round-trip', () => {
  it('round-trips a typical goal through serialize then parse', () => {
    const goal: ParsedGoal = {
      currentState: 'Nothing exists yet.',
      doneCriteria: 'Users can log in with email and password.',
      constraints: ['Use the existing auth module', 'Do not add a new dependency'],
      checklist: [
        { text: 'Add login form', checked: false },
        { text: 'Add password hashing', checked: true },
      ],
    };

    const result = parseIssueBody(serializeGoal(goal));

    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.goal).toEqual(goal);
    }
  });

  it('round-trips a goal with no constraints', () => {
    const goal: ParsedGoal = {
      currentState: 'State.',
      doneCriteria: 'Criteria.',
      constraints: [],
      checklist: [{ text: 'Only step', checked: false }],
    };

    const result = parseIssueBody(serializeGoal(goal));

    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.goal).toEqual(goal);
    }
  });

  it('round-trips multi-line current state and done criteria', () => {
    const goal: ParsedGoal = {
      currentState: 'Line one.\nLine two.',
      doneCriteria: 'First outcome.\nSecond outcome.',
      constraints: ['One constraint'],
      checklist: [{ text: 'Step', checked: true }],
    };

    const result = parseIssueBody(serializeGoal(goal));

    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.goal).toEqual(goal);
    }
  });
});
