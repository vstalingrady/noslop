---
name: noslop
description: >-
  Use when drafting or rewriting prose that should read human (articles, emails,
  stories, bios, reports, tweets, long answers), or when the user says noslop,
  write human, anti AI voice, or /noslop. Structure-first; not code cleanup.
---

# noslop

Human writing is **built** differently, not just word-swapped.

**Default:** grade structure **inline** in this session.  
**No API extract.** No OpenCode. No OpenAI. No subagents.

Surface bans: [style-and-bans.md](style-and-bans.md).

## Pipeline

```
1. WRITE (structure + bans)
2. INLINE NOSLOP GRADE (5 axes)
3. MERGE → PASS/FAIL
4. If FAIL: structural fix → re-grade once (max 2 rounds)
5. Ship
```

## Write rules

**Structure**

- Don’t preach the theme. No closing sermon.
- Don’t over-tidy. Leave friction / loose end / grey when it fits.
- Specifics: names, numbers, times, concrete nouns.
- Uneven rhythm.
- Emotion: name it sometimes; don’t only stack body metaphors.
- No “it’s not X, it’s Y” spam or restatement closers.
- Trust the reader.

**Surface** — see [style-and-bans.md](style-and-bans.md)

- No delve / tapestry / realm / pivotal / leverage / seamless / game-changer fluff.
- No “In today’s…”, “It’s worth noting…”, “At its core…”, “Here’s the thing…”.
- No Moreover/Furthermore/Additionally openers as filler.
- Em dash sparse. No rule-of-three autopilot. Contractions OK.

## Inline grade

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

**Merge:** mean of scored axes ≥ 1.2 and ≤1 FAIL → PASS.

| Axis | Fail if |
|------|---------|
| Theme | Moral/lesson stated out loud |
| Plot | Too tidy; restatement closers |
| Time | Long piece never breaks pure linear march (short → N/A) |
| Specificity | Fog only; no concrete anchors |
| Felt life | Body-catalog only; no doubt/mess/plain feeling |

## Optional local XGBoost

Only if user wants numbers and repo is installed. **You** fill features in-session (see [core_features.md](core_features.md)), write JSON, then:

```powershell
cd path\to\noslop
$env:PYTHONPATH="src"
python -m noslop.cli score --features features.json --json
```

Local only (numpy + xgboost). Never call an external extract API.

## Never

- Live API / OpenCode / OpenAI feature extract
- Spawn subagents for grading
- Synonym-only fixes when FAIL was structural
- Claim detector bypass
