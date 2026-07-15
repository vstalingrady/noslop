---
name: noslop
description: >-
  Use when drafting or rewriting user-facing prose that must not read as AI-slop,
  or when the user says noslop, write human, anti AI voice, or /noslop. Not for
  code cleanup. Primary gate is VOICE (reader anti-slop), not StoryScope P(human).
---

# noslop

Write so a careful reader doesn’t bounce. **Human flow first.** Construction + mess; bans second. Do not max scores until the page is stiff.

**Modes:** see [modes.md](modes.md). Default ship intensity = **balanced**. **max** is research only. High scores with unreadable craft = failure.

StoryScope / XGBoost is **optional diagnostic only**. Books mean ~0.13 P(human) on that scorer — a “low” StoryScope band can still be good writing.

**Violating the letter of these rules is violating the spirit of the rules.**

```
NO SHIP WITHOUT: PRE-WRITE (incl. Mode) + draft + NOSLOP VOICE (no hard_fail)
Default Mode = balanced. Do not require VOICE 9+ or StoryScope P(human) ≥ 0.5.
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

Refs: [modes.md](modes.md) · [voice.md](voice.md) · [checklists.md](checklists.md) · [style-and-bans.md](style-and-bans.md)  
Optional StoryScope: [human_coding.md](human_coding.md) · [core_features.md](core_features.md)

## PRE-WRITE (required)

```text
NOSLOP PRE-WRITE
Mode: modest | balanced | max
Audience:
Length / form:
Anchors (name / number / place / time):
One deliberate mess / open cost / incomplete beat:
One boring detail with no payoff:
What I will NOT force (skip: frame | twist | theme line | long aftermath):
Where short hits land:
Surface risk for this genre:
```

If Mode omitted → **balanced**.

## Draft recipe (by mode)

Follow [modes.md](modes.md). For **balanced** (default):

| Do | How it shows |
|----|----------------|
| Flow first | A person would finish the page without fatigue |
| Anchors | real names/times/places when they help — not a stampede |
| Uneven | one skip or digression if natural |
| No thesis close | end on image/action/cutoff |
| Clean surface | no glue/ban spam |

**modest:** lighter still — digression OK, fewer checklist beats.  
**max:** full craft pressure (research); label it; expect readability cost.

**Do not** primary-optimize StoryScope must-hit stacks or VOICE 9+ as the win condition.

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

Ship bar (**balanced**): no hard_fail; prefer score ≥ ~5.5–7. Do **not** require 9+.  
**modest:** soft; prioritize flow. **max:** research; high score OK only if labeled.

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

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “StoryScope says PASS” | Optional metric; books score ~0.13 |
| “Sounds fine to me” | Fill VOICE axes or run CLI |
| “Bans list is the skill” | Construction + mess first |
| “I’ll force the full arc pack” | Anti-template; over-complete craft still smells model-made |
