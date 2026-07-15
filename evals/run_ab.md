# A/B eval runner

## Fixed briefs

See `evals/prompts.json` (5 briefs: fiction, email, bio, SaaS, technical).

## Artifacts per brief

- `{id}_default.md` / `{id}_noslop.md` — drafts
- `{id}_*_features.json` — honest feature maps
- `{id}_*_cites.md` — span cites for high-lift IDs
- `{id}_*_score.json` — CLI score dump
- `SUMMARY.md` — table + criteria

## Re-score

```powershell
cd C:\Users\vstal\noslop
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe evals\run_score_ab.py
# or single file:
.\.venv\Scripts\python.exe -m noslop.cli score --features evals/results/mall_shoe_noslop_features.json --json
```

## Pass bars

1. noslop P(human) ≥ default + 0.15 on ≥4/5
2. noslop P(human) ≥ 0.5 on ≥3/5
