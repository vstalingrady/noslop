# noslop

Prompt-engineering skill + local StoryScope XGBoost scorer so **AI drafts can score human** on discourse construction features (arXiv:2604.03136).

## Skill

```
skills/noslop/
  SKILL.md           # PRE-WRITE → human-coding draft → features → score → FIX
  human_coding.md    # must-hit constructions (aftermath, twist, embodied, …)
  checklists.md      # templates + cite rules
  core_features.md   # lean feature pack
  style-and-bans.md  # surface polish after score loop
```

Install:

```powershell
Copy-Item -Force skills\noslop\* $env:USERPROFILE\.claude\skills\noslop\
```

Flow:

1. Fill PRE-WRITE (aftermath, end turn, embodied beat, frame, theme surface)
2. Draft so those are **true on the page**
3. Fill lean `features.json` (must-hit + support) with span cites — never forge
4. Score → if P(human) low, structural FIX (max 2 rounds)
5. Optional surface ban polish last

## Local score

```powershell
cd C:\Users\vstal\noslop
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m noslop.cli score --features features.json --json
.\.venv\Scripts\python.exe -m noslop.cli score --features features.json --min-coverage 0.05
.\.venv\Scripts\python.exe -m noslop.cli features-template --pack high-gain --out features_template.json
```

**Lean pack note:** must-hit constructions (~12–23 IDs) beat bloated mid-value fills. See `evals/results/SUMMARY.md`.

## Eval A/B

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe evals\run_score_ab.py
```

Writes per-brief default vs noslop scores into `evals/results/SUMMARY.md`.

## artifacts/

| Path | Role |
|------|------|
| `taxonomy.json` | Feature definitions |
| `encoder_state.json` | Feature → model columns |
| `models/noslop_binary_narrative.json` | Trained detector |
| `human_coding_targets.json` | Must-hit / support / high-gain pack |

Model weights are **not** retrained for the skill loop.

## License

MIT. StoryScope attribution: `THIRD_PARTY_NOTICES.md`.
