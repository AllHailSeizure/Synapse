---
name: synapse:speccing-first
description: Approach to clarifying intent and spec before implementation. Focus on understanding behavior, not building.
type: behavior
applies_to: [all coding projects]
---

# Speccing-First

This skill describes how we approach feature spec and requirements clarification before building.

## Approach

When a user describes a feature or asks to implement something:

1. **Understand behavior, not implementation.** What should this *do*? What's the input, output, constraints?
2. **Ask clarifying questions.** One at a time. Focus on: purpose, success criteria, constraints, edge cases.
3. **Propose approaches.** 2-3 options with trade-offs. Lead with a recommendation.
4. **Get alignment.** Make sure the user agrees on what we're building before we build it.
5. **Write the spec.** Brief but complete—what we're building, constraints, how to know it works.

## Key Principles

- **Spec is a contract.** Once we agree on spec, implementation follows it faithfully. No surprises.
- **Questions before code.** Always clarify before writing implementation.
- **Short spec, not detailed.** A few sentences for simple features, a paragraph or two for complex ones. Just enough to remove ambiguity.
- **Include success criteria.** How do we know this works? What tests pass?

## Example Conversation

**User:** "I need a search function."

**Response:** "Let me clarify. Search for what—documents? Code? In what fields? How exact does the match need to be? Just substring, or fuzzy? Should it be case-sensitive? And what's the output—just a list of results, or with relevance scores?"

**User:** "Search documents by title and content, case-insensitive substring match, returns list of matching documents sorted by relevance."

**Response:** "Got it. One more thing: what determines relevance? Title matches rank higher than content? Or is it based on how many times the term appears?"

**User:** "Title matches rank higher."

**Spec to document:**
```
Search feature:
- Input: search term (string)
- Search: document titles and content (case-insensitive substring match)
- Ranking: matches in titles before matches in content
- Output: list of matching documents, sorted by relevance
- Success: search("react") returns documents with "react" in title or content, titles first
```

Now we build to this spec, no surprises.

---

## Integration

Use this skill whenever spec is unclear. It's collaborative—you're helping the user think through what they actually want, not lecturing them on how to write requirements.
