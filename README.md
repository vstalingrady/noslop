# noslop

Score writing the way [StoryScope](https://arxiv.org/abs/2604.03136) does: discourse features in, human-vs-AI probability out. Plus a small agent skill that refuses to ship prose without that score.

## Paper

Russell, Rajendhran, Pham, Iyyer, Wieting. **StoryScope: Investigating idiosyncrasies in AI fiction.** arXiv:[2604.03136](https://arxiv.org/abs/2604.03136), 2026.

Code (MIT): [jenna-russell/storyscope](https://github.com/jenna-russell/storyscope)

Their result worth knowing: narrative features alone hit **93.2% macro-F1** for human vs AI on long fiction (~5k words). Style cues help, but structure still carries most of the signal after surface cleanup.

We wrap that idea for agents:

1. Extract the same **304-feature taxonomy** (LLM feature application, 10 dimension calls)
2. Encode + run **XGBoost** with the paper’s binary hyperparameters
3. Gate agent drafts: pass only if P(human) clears the threshold

See `THIRD_PARTY_NOTICES.md` for StoryScope attribution.

## Deps (kept thin)

Runtime score path:

```
numpy
xgboost
```

That’s it. No sklearn stack for day-to-day scoring.

Optional:

```
pip install pyarrow     # train / rebuild from parquet once
# OPENAI_API_KEY + network for live feature extract
```

## Setup

```powershell
cd C:\Users\vstal\noslop
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH="src"
```

Artifacts already in repo (or rebuild):

```powershell
python -m noslop.tools.build_encoder
# once, needs pyarrow + StoryScope feature parquet:
pip install pyarrow
python -m noslop.tools.train_binary --subset narrative
```

## Score

```powershell
# offline if you already have feature JSON from StoryScope extract
python -m noslop.cli score draft.md --features features.json

# live extract (needs OPENAI_API_KEY; ~10 LLM calls)
python -m noslop.cli score draft.md
python -m noslop.cli score draft.md --json
python -m noslop.cli score draft.md --model full
```

Exit codes: `0` PASS (human-ish), `1` FAIL (AI-ish), `2` setup/error.

Default model: `noslop_binary_narrative.json` (style features dropped, paper’s main claim).

**Note on weights.** Upstream `binary_narrative.json` ships with StoryScope but uses a column layout they didn’t fully publish with the open train script. We train `noslop_binary_*.json` on their released feature matrix with paper hyperparams so encode → predict is consistent. Same science, runnable gate.

## Domain limit

StoryScope trained on **long fiction**. A 40-word tweet is out of distribution. Use this on articles, stories, long emails, reports. Short chat fluff will look weird; the skill says so.

## Agent skill

Copy or link:

```
skills/noslop/  →  ~/.claude/skills/noslop/
```

Triggers: `noslop`, write human, anti AI voice, `/noslop`.

Loop the skill enforces:

```
draft → noslop score → fix if FAIL → re-score (max 2) → ship with evidence
```

No “I self-checked.” Exit code or JSON only.

## Cost

| Step | Cost |
|------|------|
| XGBoost predict | free, local, ms |
| Feature extract | ~10 LLM calls / document |
| Train once | local CPU/GPU time on parquet |

## Layout

```
noslop/
  src/noslop/          CLI + score path
  artifacts/           taxonomy, models, encoder_state
  third_party/storyscope/   git submodule (MIT)
  skills/noslop/       agent skill
  tests/
```

## License

MIT for noslop wrapper + skill. StoryScope remains MIT © Jenna Russell et al.; we vendor it under `third_party/`.
