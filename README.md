# noslop

**Skill** for structure-first human-ish prose (inline grade + style bans).  
Optional **local XGBoost** score from feature JSON only.

Inspired by [StoryScope](https://arxiv.org/abs/2604.03136). No live API extract.

## Skill (default)

```
skills/noslop/
  SKILL.md
  style-and-bans.md
  core_features.md
```

Copy to `~/.claude/skills/noslop/`.

Host agent writes + grades inline. No network.

## Local score (optional)

```
numpy
xgboost
```

```powershell
cd C:\Users\vstal\noslop
pip install -r requirements.txt
$env:PYTHONPATH="src"
python -m noslop.cli score --features features.json --json
```

Agent fills features (see `core_features.md`); CLI is local only.

### Retrain

```powershell
# download StoryScope storyscope_features.parquet → artifacts/
pip install pyarrow
python -m noslop.tools.build_encoder
python -m noslop.tools.train_binary --subset narrative
```

## Layout

```
skills/noslop/     skill
src/noslop/        local score CLI
artifacts/         taxonomy, encoder, noslop_binary_*.json
tests/             encode width tests
```

## License

MIT (noslop). StoryScope attribution: `THIRD_PARTY_NOTICES.md`.
