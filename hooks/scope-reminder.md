SCOPE BOUNDARY: do only what this turn asked.

Found a bug, a stale doc, or something else worth fixing while working? Leave it
and keep going — do not diagnose, fix, write a test for, capture it, or otherwise
chase it unless the user asks for that in this turn. They file sticky-note bugs
with Cursor `/bug`, `/patch`, or the matching `commands/*.mjs` scripts; do not
decide to run those yourself.

Same for verification: don't run a full test suite, audit, or fact-check pass you weren't
asked for. A targeted run to debug one specific thing is fine; "let me verify everything
first" is not.
