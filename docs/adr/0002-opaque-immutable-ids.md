# 2. Pages are identified by opaque, immutable ids, never by filename

**Status:** accepted (2026-11-08)

## Context
Titles change as understanding improves. If links pointed at filenames or titles, every rename would break relations, citations and flashcard history.

## Decision
Every page gets an id such as `cpt_k3x9a2mq` from `./kb new`. Relations, citations and learning records reference ids only. A target that has no page yet is written `unresolved: "Name"`, never a guessed id.

## Consequences
- Renaming a page breaks nothing except `[[wikilinks]]` in prose, which validation checks.
- An id says nothing to a reader, so tools must always show the title next to it.
- The model cannot invent a plausible-looking link: an unknown id is a validation error.

## Revisit when
Never, short of a full export to another system; ids are the one thing that must not change.
