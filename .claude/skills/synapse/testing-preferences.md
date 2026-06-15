---
name: synapse:testing-preferences
description: Testing philosophy and approach for Synapse projects—when to test, what to test, how to structure tests.
type: behavior
applies_to: [all coding projects]
---

# Testing Preferences

## Philosophy

Tests verify behavior. A test should answer: "Does this code do what it's supposed to do?"

Tests are not:
- Proof of 100% code coverage (coverage is a tool, not a goal)
- Verification of implementation details (test the interface, not the internals)
- Busywork (if a test doesn't provide confidence in behavior, don't write it)

## When to Write Tests

**Critical paths:** Always test the happy path and edge cases for anything users rely on.

**Behavior you're uncertain about:** Use tests to explore the design (TDD-style).

**Refactoring:** Write tests first to lock down behavior, then refactor confidently.

**Bug fixes:** Add a test that reproduces the bug, fix the code, verify test passes.

## Test Structure

One test, one behavior assertion:

```python
def test_search_returns_matching_documents():
    results = search("react")
    assert len(results) > 0
    assert all("react" in doc.title or "react" in doc.content for doc in results)
```

Not:

```python
def test_search():
    # Tests search, parsing, ranking, filtering all at once
    ...
```

## Coverage Goals

Aim for confidence, not a number. Generally:
- **Core logic:** 80%+ coverage
- **Error handling:** Cover the main error paths
- **Edge cases:** If it can break, test it

But 60% coverage of the right code is better than 95% coverage of busywork.

## Test Frameworks

Use what the project already uses. If starting fresh:

**JavaScript/TypeScript:** Jest or Vitest
**Python:** pytest
**Go:** stdlib testing + testify for assertions
**Others:** Language convention

---

## Integration

Before implementing a feature, consider: How will we know it works? Write those tests first, implement to pass them.
