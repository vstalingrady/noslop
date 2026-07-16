# StoryScope human-coding (lab only)

Optional diagnostic path. **Not a ship recipe.**  
**Writing long fiction uses [construction.md](construction.md)** (PRE-STRUCTURE, sparse moves, page judgment). This file is only for honest feature scoring when asked.

Ship = construction or short-prose flow + no VOICE hard_fail + careful reader finishes the page ([paper.md](paper.md), [SKILL.md](SKILL.md)).

Use when:

1. User asks for StoryScope / P(human) diagnostics, **and**
2. Text is long enough for discourse features (prefer ~1k–5k+ words fiction), **or** research evals.

## Context

- Paper measured **construction** on ~5k-word parallel stories; features **extracted**, not forged.
- Local books mean ~**0.13** P(human) (`evals/results/HUMAN_BASELINE.md`) and still read as human.
- Forced must-hit stacks can raise the binary while prose stays stiff — score farming, not skill success.
- Never require P(human) ≥ 0.5 to ship.
- Higher P(human) is **not** “more human.”

## Labeling rules

1. Label only what is **true on the page** (span cites).
2. Never invent features to raise score.
3. Short agent prose: usually **skip** this path.
4. Report score as a **footnote**, never sole gate.

## Construction notes (long fiction)

Prefer the full method in [construction.md](construction.md). Lab shorthand:

| Prefer | Avoid |
|--------|--------|
| Theme in scene / action | Narrator explains the lesson |
| Grey / open moral cost | Tidy single-track acceptance bow |
| Temporal texture if length allows | Fake flashbacks in a postcard |
| Named world / specific mess | Vague “philosophy dialogue” default |
| Diversity across drafts (seed) | One winning feature pack every time |

## Optional diagnostic table

Only mark a row if the draft **shows** it.

| ID | Idea | Only if true on page |
|----|------|----------------------|
| SIT_MET_303 | Theme not over-explained | theme in scene, not TED close |
| PLT_* / resolution | Not only tidy protagonist bow | open cost or multi-track if present |
| TMP_* | Temporal complexity | real jumps/flashbacks — don’t invent |
| AGENT_EMO_009 | Embodied emotion | body words present; don’t spam formula |
| SIT_MET_008 | World echoes | real brand/song/place — not filler |

Fill with span cites via [core_features.md](core_features.md). Score:

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m noslop.cli score --features features.json --json
```

## Do not

- Forge features  
- Use this checklist as PRE-WRITE for emails  
- Ship or fail ship on P(human)  
- Treat this file as a must-hit writing coach  
- Retrain or “improve” by gaming the binary  
