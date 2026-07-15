---
name: noslop
description: >-
  Use when drafting or rewriting user-facing prose that must score human on
  StoryScope / noslop P(human), or when the user says noslop, write human,
  anti AI voice, or /noslop. Not for code cleanup.
---

# noslop

AI text can score **human** when construction matches human narrative coding —
not when you only ban “delve” or leave every thread open.

**Violating the letter of these rules is violating the spirit of the rules.**

```
NO SHIP WITHOUT: PRE-WRITE + draft with human-coding in PROSE + features.json
(with span cites) + CLI score evidence
```

## When to use

- Stories, emails, bios, reports, landing copy, long agent answers
- User wants human-sounding text / higher StoryScope P(human)

## When not to use

- Code cleanup
- Pure data dumps where voice does not matter

## Core pattern

```
1. Fill NOSLOP PRE-WRITE (include aftermath, twist, embodied beat, frame)
2. Draft so human_coding.md targets are visible in the prose
3. Fill features.json (high-gain pack fully) — each value needs a cited span
4. Run CLI score (repo venv, PYTHONPATH=src)
5. FAIL or P(human) < 0.5 → structural FIX targeting feature gaps (max 2 rounds)
6. Ship draft + features + score JSON
```

References:

- [human_coding.md](human_coding.md) — must-hit constructions
- [checklists.md](checklists.md) — PRE-WRITE / GRADE / SCORE templates
- [core_features.md](core_features.md) — feature IDs to fill
- [style-and-bans.md](style-and-bans.md) — surface polish **after** score loop

## PRE-WRITE (required)

```text
NOSLOP PRE-WRITE
Audience:
Length / form:
Specific anchors (name / number / place / time):
Aftermath plan (what happens after climax — required):
End turn / twist (what recontextualizes the piece):
Embodied emotion beat (body + sensation):
Frame device if any (log / later tell / none):
Theme surface (where meaning is allowed to show — not silent):
Rhythm note:
Surface risk:
```

Then write so every filled line is visible in the draft.

## Draft recipe (human-coding)

| Do | How it shows |
|----|----------------|
| Extended aftermath | Second scene or time-jump after the peak |
| End turn | Late reframe of the object, choice, or claim |
| Embodied feeling | Cold tile, weight in hand, throat — not only “sad” |
| Theme surface | Thought/speech lets meaning show (level 3–4) — not zero, not pure lecture |
| Frame when possible | Log, memoir, “I’m writing this after…” |
| Anchors | Names, numbers, clock times, places |
| World echo | Song, brand, local detail, cultural gesture |
| Vary rhythm | Short hits beside longer sentences |

**Do not primary-optimize** “leave fully open / never state theme / cut at climax.” Those tank StoryScope P(human).

## Feature fill (required for score)

1. Load high-gain pack from [core_features.md](core_features.md) / `artifacts/human_coding_targets.json`.
2. For each ID, set a taxonomy value **only if** a draft span supports it.
3. Record cites: `ID — "quoted span…"`.
4. Never forge.

## SCORE (required)

```powershell
cd path\to\noslop
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m noslop.cli score --features features.json --json
```

```text
NOSLOP SCORE
coverage: x.xx
P(human): x.xx
gate: PASS|FAIL
gaps: (feature IDs that should be true in prose but aren't)
FIX: structural bullets targeting gaps
```

Ship bar (eval / strict use): prefer **P(human) ≥ 0.5** and high-gain pack fully filled.

## GRADE (structure checklist)

Still fill structure grade from [checklists.md](checklists.md). Structure FAIL → fix before celebrating a lucky score.

## Red flags — STOP

- Shipping without PRE-WRITE or score evidence
- Feature values without span cites
- FIX = synonym swaps while construction gaps remain
- Hard cut at climax with no aftermath
- Theme totally silent **or** pure moral essay with no scene
- Skipping score because “it sounds fine”

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “Open ending is more literary” | This scorer rewards aftermath + turn; write those |
| “I’ll just edit the JSON” | Forgery fails honesty; rewrite the prose |
| “Bans list is the skill” | Construction first; bans second |
| “Sparse features are fine” | Fill high-gain pack; sparse maps floor P(human) |
