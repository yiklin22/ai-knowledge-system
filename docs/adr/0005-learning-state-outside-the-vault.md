# 5. Learning progress lives in SQLite, outside the vault

**Status:** accepted (2026-11-08)

## Context
Flashcard schedules, mastery levels and misconceptions change every study session. Knowledge pages change rarely and only after review.

## Decision
Recall cards are written on concept pages and synced into `data/learning.db`. Scheduling state, mastery and tutor records live only in that database. Tutor sessions never edit `vault/`.

## Consequences
- Studying produces no Git noise and cannot damage knowledge.
- The database is private and not committed, so it needs its own backup.
- Deleting it loses progress but no knowledge; cards are recreated from the pages.

## Revisit when
Progress has to sync between machines.
