# noslop

Structure-first writing skill for agents, plus a local XGBoost scorer for narrative human-vs-AI features.

Design draws on [StoryScope](https://arxiv.org/abs/2604.03136) (discourse construction over surface style).

## Skill

```
skills/noslop/
  SKILL.md           # recipe + iron law
  checklists.md      # PRE-WRITE + GRADE templates
  style-and-bans.md  # surface reference
  core_features.md   # feature IDs for local score
```

Install:

```
copy skills\noslop\*  %USERPROFILE%\.claude\skills\noslop\
```

Flow: fill PRE-WRITE → draft → fill GRADE → fix until PASS → ship.

## Local score

Runtime: `numpy`, `xgboost`.

```powershell
cd C:\Users\vstal\noslop
pip install -r requirements.txt
$env:PYTHONPATH="src"
python -m noslop.cli score --features features.json --json
```

Pass a feature map JSON (see `core_features.md`). The CLI scores offline with the bundled model.

### Retrain

Place StoryScope `storyscope_features.parquet` in `artifacts/`, then:

```powershell
pip install pyarrow
python -m noslop.tools.build_encoder
python -m noslop.tools.train_binary --subset narrative
```

## artifacts/

Offline scorer data (skill does not load these):

| Path | Role |
|------|------|
| `taxonomy.json` | Feature definitions |
| `encoder_state.json` | Feature → model columns |
| `models/noslop_binary_narrative.json` | Trained detector |

## Layout

```
skills/noslop/   agent skill
src/noslop/      local score CLI
artifacts/       taxonomy, encoder, model
tests/           encode/score tests
```

## License

MIT. StoryScope attribution: `THIRD_PARTY_NOTICES.md`.
