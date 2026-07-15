---
name: noslop
description: >-
  Use when drafting or rewriting user-facing prose that must not read as AI-slop,
  or when the user says noslop, write human, anti AI voice, or /noslop. Not for
  code cleanup. Primary gate is VOICE (reader anti-slop), not StoryScope P(human).
---

# noslop

Write so a careful reader doesn’t bounce. Construction + mess first. Bans second.

StoryScope / XGBoost is **optional diagnostic only**. High P(human) is not “sounds like a book” — books mean ~0.13 on that scorer; see `evals/results/HUMAN_BASELINE.md`. GPTZero can still flag AI. Do not claim undetectable.

**Violating the letter of these rules is violating the spirit of the rules.**

```
NO SHIP WITHOUT: PRE-WRITE + draft + NOSLOP VOICE (MERGED: PASS)
StoryScope score is NOT required for ship.
```

## When to use

- Stories, emails, bios, reports, landing copy, long agent answers
- User wants human-sounding / less slop / noslop

## When not to use

- Code cleanup
- Pure data dumps where voice does not matter

## Core pattern

```
1. Fill NOSLOP PRE-WRITE
2. Draft so PRE-WRITE lines show on the page
3. Fill NOSLOP VOICE grade (or run CLI voice)
4. FAIL → structural FIX only (max 2 rounds) — not synonym swaps
5. Surface ban scan (style-and-bans.md) once
6. Optional: StoryScope features + score (diagnostic footnote only)
7. Ship with VOICE evidence
```

Refs: [voice.md](voice.md) · [checklists.md](checklists.md) · [style-and-bans.md](style-and-bans.md)  
Optional StoryScope: [human_coding.md](human_coding.md) · [core_features.md](core_features.md)

## PRE-WRITE (required)

```text
NOSLOP PRE-WRITE
Audience:
Length / form:
Anchors (name / number / place / time):
One deliberate mess / open cost / incomplete beat:
One boring detail with no payoff:
What I will NOT force (skip: frame | twist | theme line | long aftermath):
Where short hits land:
Surface risk for this genre:
```

## Draft recipe (VOICE-first)

| Do | How it shows |
|----|----------------|
| Anchors | real names, times, places, numbers |
| Uneven | one skip, digression, or dead-end detail |
| No thesis close | end on image/action/cutoff |
| Rhythm | short next to long |
| Feeling | body or behavior — not only “sad” |
| Optional frame/twist | only if natural — not a checklist dump |

**Do not primary-optimize** StoryScope must-hit stack (extended aftermath + theme-4 + climactic twist + memoir frame every time). That games the old scorer and still smells model-made.

## VOICE grade (required)

```text
NOSLOP VOICE
anchors:     0-2  PASS|FAIL
uneven:      0-2  PASS|FAIL
moral_close: 0-2  PASS|FAIL   (2 = clean)
rhythm:      0-2  PASS|FAIL
glue_bans:   0-2  PASS|FAIL
MEAN: x.x
HARD: none | moral_close_sermon | ban_spam | zero_anchors
MERGED: PASS|FAIL
FIX: …
```

CLI (preferred when available):

```powershell
cd path\to\noslop
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m noslop.cli voice --text-file draft.md --json
```

Ship bar: **score ≥ 6.5** and no hard_fail.

## StoryScope mode (optional)

Only if user asks for StoryScope / P(human) diagnostic:

1. Fill features with span cites ([core_features.md](core_features.md))
2. `python -m noslop.cli score --features features.json --json`
3. Report as footnote — **never sole ship gate**
4. Do not require P(human) ≥ 0.5 for ship

## Red flags — STOP

- Shipping without PRE-WRITE or VOICE PASS
- Chasing StoryScope 0.5 while VOICE fails
- FIX = synonym swaps only
- Thesis closer as last paragraph
- Zero anchors on long prose
- Ban/glue spam
- Claiming GPTZero-proof

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “StoryScope says PASS” | Optional metric; books score ~0.13 |
| “Sounds fine to me” | Fill VOICE axes or run CLI |
| “Bans list is the skill” | Construction + mess first |
| “I’ll force the full arc pack” | Anti-template; detectors still catch it |
