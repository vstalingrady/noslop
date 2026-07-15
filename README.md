# noslop

Agent skill for **structure-first** human-ish prose, plus optional **local** XGBoost score from feature JSON.

Inspired by [StoryScope](https://arxiv.org/abs/2604.03136) (Russell et al.). No live LLM API extract.

## Paper

Russell, Rajendhran, Pham, Iyyer, Wieting. **StoryScope: Investigating idiosyncrasies in AI fiction.** arXiv:[2604.03136](https://arxiv.org/abs/2604.03136).

Code (MIT): [jenna-russell/storyscope](https://github.com/jenna-russell/storyscope)

See `THIRD_PARTY_NOTICES.md`.

## Two paths

### 1. Skill (default — fast)

`skills/noslop/` — write with structure rules + style bans, **inline** `NOSLOP GRADE`.  
Host agent only. No network. No XGBoost required.

```
skills/noslop/SKILL.md
skills/noslop/style-and-bans.md
skills/noslop/core_features.md
skills/noslop/graders.md
```

Install: copy to `~/.claude/skills/noslop/`.

### 2. Local XGBoost (optional numbers)

Runtime:

```
numpy
xgboost
```

```powershell
cd C:\Users\vstal\noslop
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH="src"

# features JSON produced by the host agent (or offline tools)
python -m noslop.cli score --features features.json --json
```

**No OpenCode / OpenAI / live extract.** Pass `--features` always.

Train once (needs `pyarrow` + StoryScope parquet in submodule):

```powershell
python -m noslop.tools.build_encoder
pip install pyarrow
python -m noslop.tools.train_binary --subset narrative
```

Default model: `artifacts/models/noslop_binary_narrative.json`.

Exit: `0` PASS, `1` FAIL, `2` error.

## Layout

```
noslop/
  skills/noslop/       agent skill (inline grade + bans)
  src/noslop/          local score CLI
  artifacts/           taxonomy, encoder, models
  third_party/storyscope/   git submodule
  tests/
```

## License

MIT for noslop. StoryScope MIT © Jenna Russell et al. under `third_party/`.
