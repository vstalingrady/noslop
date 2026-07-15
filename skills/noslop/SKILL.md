---
name: noslop
description: >-
  Use when drafting or rewriting prose that should read human (articles, emails,
  stories, bios, reports, tweets, long answers), or when the user says noslop,
  write human, anti AI voice, or /noslop. Structure-first; not code cleanup.
---

# noslop

Human writing is **built** differently, not just word-swapped.  
Grade structure **inline** in the same turn. **Do not spawn subagents.**

## Pipeline

```
1. WRITE under structure rules
2. INLINE grade on 5 axes (same response / same context)
3. MERGE → PASS or FAIL
4. If FAIL: fix structure only → re-grade once more (max 2 rounds)
5. Ship. Do not invent a pass.
```

Short text (tweets, one-liners) is fine. Use N/A on axes that need length.

## Write rules (structure)

- Don’t preach the theme. No closing sermon.
- Don’t over-tidy. Leave friction, a loose end, or grey choice when it fits.
- Specifics: names, numbers, times, concrete nouns.
- Uneven rhythm. Mix short and long.
- Emotion: name it sometimes. Don’t only stack body metaphors.
- No template rhetoric stacks (“it’s not X, it’s Y” spam, restatement closers).
- Trust the reader.

## Inline grade (5 axes)

After the draft, score all five in one block. No separate agents.

| Axis | Fail if |
|------|---------|
| **Theme** | States the moral/lesson; over-explains meaning |
| **Plot** | Too clean resolution; single-track; paras restate themselves |
| **Time** | Long piece never breaks pure linear march (short → N/A ok) |
| **Specificity** | Only abstract claims; no names/numbers/places/objects |
| **Felt life** | Emotion only body-catalog; no doubt/mess/plain feeling |

### Output shape (required)

```text
NOSLOP GRADE
Theme:       SCORE 0-2  PASS|FAIL|N/A  — one line why
Plot:        SCORE 0-2  PASS|FAIL|N/A  — one line why
Time:        SCORE 0-2  PASS|FAIL|N/A  — one line why
Specificity: SCORE 0-2  PASS|FAIL|N/A  — one line why
Felt life:   SCORE 0-2  PASS|FAIL|N/A  — one line why
MEAN: x.x   (ignore N/A)
MERGED: PASS|FAIL
FIX: (if FAIL) bullet structural fixes only
```

**Merge:** mean of scored axes ≥ 1.2 and ≤1 FAIL → PASS. Else FAIL.

On FAIL: apply FIX, rewrite, re-grade. Max 2 full grade rounds.

## Optional: local XGBoost scorer

Not part of the default skill path. Only if someone runs the repo CLI.

**Runtime (score with precomputed features or after extract):**

```
numpy>=1.24
xgboost>=2.0
```

**Not required for this skill’s inline grade.**

Train/extract extras (repo only): `pyarrow` for training from parquet; API key if using live feature extract. See repo README.

```powershell
cd path\to\noslop
pip install numpy xgboost
$env:PYTHONPATH="src"
python -m noslop.cli score draft.md --features feats.json
```

## Never

- Spawn subagents / fan-out graders for noslop
- Ship without NOSLOP GRADE when the user asked for noslop / human prose
- Synonym-only “fixes” when FAIL was structural
- Claim detector bypass
- Confuse with code deslop tools
