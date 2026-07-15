---
name: noslop
description: >-
  Use when drafting or rewriting user-facing prose that must not read as AI-slop,
  or when the user says noslop, write human, anti AI voice, or /noslop. Not for
  code cleanup.
---

# noslop

Human writing is built differently — construction first, polish second.

**Violating the letter of these rules is violating the spirit of the rules.**

```
NO SHIP WITHOUT FILLED PRE-WRITE + NOSLOP GRADE (MERGED: PASS)
```

## When to use

- Articles, emails, stories, bios, reports, tweets, long agent answers
- User wants human-sounding text / noslop / anti AI voice

## When not to use

- Code cleanup or refactor “deslop”
- Pure data dumps where voice does not matter

## Core pattern

Positive contracts, not ban lists.

```
1. Fill NOSLOP PRE-WRITE (create checklist for THIS piece)
2. Draft to satisfy those slots
3. Fill NOSLOP GRADE (required shape)
4. FAIL → structural FIX only → re-grade (max 2 rounds)
5. Ship with grade evidence in-thread
```

Templates: [checklists.md](checklists.md)  
Surface reference: [style-and-bans.md](style-and-bans.md)  
Local score features: [core_features.md](core_features.md)

## PRE-WRITE (required)

Emit and fill before drafting:

```text
NOSLOP PRE-WRITE
Audience:
Length / form:
Specific anchors I will use (name / number / place / time — at least one):
One deliberate mess, grey choice, or open thread:
How theme will be shown (not stated):
Rhythm note (where short hits land):
Surface risk for this genre (one line):
```

Then write so every filled line is visible in the draft.

## Draft recipe

Build toward human construction:

| Do | How it shows |
|----|----------------|
| Trust the reader | Meaning in action/image, not a lesson line |
| Leave friction when real | Open thread, grey choice, or cost |
| Anchor | Names, numbers, times, places |
| Vary rhythm | Short hits beside longer sentences |
| Name feeling sometimes | Not only body metaphors |
| End clean | No paragraph that only restates itself |

Heavy surface list lives in style-and-bans.md — load for polish, not as the whole skill.

## GRADE (required)

```text
NOSLOP GRADE
Theme:       SCORE 0-2  PASS|FAIL|N/A  — one line
Plot:        SCORE 0-2  PASS|FAIL|N/A  — one line
Time:        SCORE 0-2  PASS|FAIL|N/A  — one line
Specificity: SCORE 0-2  PASS|FAIL|N/A  — one line
Felt life:   SCORE 0-2  PASS|FAIL|N/A  — one line
MEAN: x.x
MERGED: PASS|FAIL
FIX: …
```

Merge: mean of scored axes ≥ 1.2 and ≤1 FAIL → PASS. Details in checklists.md.

## Local score

For a numeric human-vs-AI gate: fill features per core_features.md, write JSON, run:

```powershell
cd path\to\noslop
$env:PYTHONPATH="src"
python -m noslop.cli score --features features.json --json
```

Requires local XGBoost and `--features` JSON. Host agent supplies the feature map.

## Red flags — STOP

- Shipping without PRE-WRITE or GRADE
- Grade missing MERGED line
- FIX is synonym swaps while structure failed
- “Sounds fine” without filled checklists
- Skipping grade because the piece is short (still grade; use N/A on Time if needed)
- “Just this once” / “user is in a hurry”

**All of these mean: fill checklists, then ship.**

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “Too short to grade” | Grade; N/A only where form cannot support the axis |
| “I’ll polish bans first” | Structure checklists first; bans second |
| “I already know it’s human” | Evidence = filled PRE-WRITE + GRADE PASS |
| “Recipe slows me down” | Faster than rewrite loops after user smells slop |
| “Bans list is the skill” | Bans are reference; construction is the skill |

## Common mistakes

- Writing the draft before PRE-WRITE
- Stating the moral in the last paragraph
- Abstract “professional” voice with zero anchors
- Uniform sentence length across the piece
- Treating MERGED: FAIL as optional
