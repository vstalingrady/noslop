---
name: noslop
description: >-
  Use when drafting or rewriting prose that should read human (articles, emails,
  stories, bios, reports, tweets, long answers), or when the user says noslop,
  write human, anti AI voice, or /noslop. Structure-first; not code cleanup.
---

# noslop

Human writing is **built** differently, not just word-swapped.

**Fast path (default):** you grade structure **inline** in this session.  
**No second API.** No OpenCode. No subagents. No 10-dimension HTTP fan-out.

## Why not API extract every time?

Live StoryScope extract = ~10 LLM calls over the network → slow, 502s, cost.  
You are already an LLM in Claude Code / Cursor / whatever. **Use this turn.**

Optional local XGBoost is only for offline numbers after **you** emit a features JSON.

## Pipeline (default — fast)

```
1. WRITE under structure rules
2. INLINE grade (5 axes) in the same response
3. MERGE → PASS/FAIL
4. If FAIL: structural fix → re-grade once (max 2 rounds)
5. Ship
```

### Write rules

- Don’t preach the theme. No closing sermon.
- Don’t over-tidy. Leave friction / loose end / grey when it fits.
- Specifics: names, numbers, times, concrete nouns.
- Uneven rhythm.
- Emotion: name it sometimes; don’t only stack body metaphors.
- No “it’s not X, it’s Y” spam or restatement closers.
- Trust the reader.

### Inline grade block

```text
NOSLOP GRADE
Theme:       SCORE 0-2  PASS|FAIL|N/A  — one line
Plot:        SCORE 0-2  PASS|FAIL|N/A  — one line
Time:        SCORE 0-2  PASS|FAIL|N/A  — one line  (short text → N/A ok)
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
| Time | Long piece never breaks pure linear march |
| Specificity | Fog only; no concrete anchors |
| Felt life | Body-catalog only; no doubt/mess/plain feeling |

## Optional: local XGBoost (still no second API)

Only if the user wants a **numeric** gate and the `noslop` repo is installed.

1. **You** (this agent) fill StoryScope feature values from the draft — in this session, one shot or by dimension. Write `features.json` as `{"features": { "ID": value, ... }}`.  
2. Run **local only** (ms, numpy+xgboost):

```powershell
cd path\to\noslop
$env:PYTHONPATH="src"
python -m noslop.cli score draft.md --features features.json --json
```

Do **not** call OpenCode/OpenAI for extract unless the user explicitly asks for “live API extract”.

### Faster XGBoost variant

Full 304 features is heavy even for you. Prefer:

- **Narrative-only** IDs (skip `STY_*`), or  
- High-signal subset from `skills/noslop/core_features.md` if present  

Missing IDs encode as empty/zero; still better than a 10-minute HTTP extract.

## Never

- Spawn subagents for grading  
- Default to live API feature extract  
- Synonym-only fixes when FAIL was structural  
- Claim detector bypass  

## Repo note

`noslop` CLI + OpenCode Go env still exist for batch/research extract. **Skill default = host model + optional local score.**
