# Feature IDs (StoryScope diagnostic only)

**v2:** Optional. Ship does **not** require filling these or P(human) ≥ 0.5.

Primary gate: `python -m noslop.cli voice --text-file draft.md --json`

## When to use

User explicitly wants StoryScope / discourse-feature score.

```powershell
$env:PYTHONPATH="src"
python -m noslop.cli features-template --pack high-gain --out features.json
# fill from draft with cites
python -m noslop.cli score --features features.json --json
```

## Lean pack

Prefer must-hit + support from `artifacts/human_coding_targets.json`.  
Bloated mid-value fills can **lower** P(human). See [human_coding.md](human_coding.md).

## Honesty

Each filled ID needs a quoted span from the draft. Forge → invalid diagnostic.

## Books baseline

Mean P(human) on classic excerpts ~**0.13**. Do not treat gate PASS as literary quality.
