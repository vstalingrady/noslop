# noslop Score-Human Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the noslop skill and scoring workflow so prompt-engineered AI drafts score substantially higher **P(human)** on the local StoryScope XGBoost scorer than default drafts.

**Architecture:** Align skill PRE-WRITE/draft/GRADE with human-coding feature targets discovered from model gain sweeps; add feature-template + coverage-honest scoring; closed loop draft→fill→score→FIX; prove with A/B eval.

**Tech Stack:** Python 3.11, XGBoost (existing), taxonomy JSON, skill markdown under `skills/noslop/`, CLI `python -m noslop.cli`.

**Spec:** `docs/superpowers/specs/2026-07-15-noslop-score-human-design.md`

---

## File map

| Path | Role |
|------|------|
| `skills/noslop/SKILL.md` | Main agent recipe (rewrite) |
| `skills/noslop/checklists.md` | PRE-WRITE / GRADE / feature-cite rules |
| `skills/noslop/core_features.md` | Expand to high-gain pack + fill rules |
| `skills/noslop/human_coding.md` | **Create** — construction targets mapped to feature IDs |
| `skills/noslop/style-and-bans.md` | Keep; polish only after score loop |
| `src/noslop/cli.py` | Add `features-template`, coverage gate flags |
| `src/noslop/score.py` | Coverage warning + optional refuse-PASS if sparse |
| `src/noslop/report.py` | Print coverage + top filled human-coding hits |
| `evals/prompts.json` | **Create** — A/B briefs |
| `evals/run_ab.md` | **Create** — how to run A/B by hand/agent |
| `README.md` | Document new flow |
| Mirror skill → `~/.claude/skills/noslop/` after change | Install |

---

### Task 1: Freeze human-coding reference from model

**Files:**
- Create: `skills/noslop/human_coding.md`
- Create: `artifacts/human_coding_targets.json` (machine-readable for CLI later)

- [ ] **Step 1: Write `human_coding.md`** with the locked targets (from design + sweep):

```markdown
# Human-coding targets (StoryScope narrative model)

Write prose so these are *true*, then label them in features.json.

## Must-hit (high lift)
| ID | Prefer value | How it shows in prose |
|----|--------------|------------------------|
| PLT_MOR_007 | extended aftermath | After climax, ≥1 scene/time-jump of consequence |
| SIT_MET_303 | 3 or 4 | Theme surfaces in thought/speech; not silent, not pure TED talk |
| REV_SUR_007 | climactic_end_twist | Late turn recontextualizes object/choice |
| EVT_SCH_010 | include frame_confession/memoir when possible | Log, later recollection, framed telling |
| AGENT_EMO_009 | embodied_sensations_and_metaphors | Body + sensation for feeling |
| SIT_MET_008 | Balanced mix… or Primarily implicit echoes | One real-world echo (song, brand, local detail) |

## Strong support
| ID | Prefer | Prose |
|----|--------|-------|
| TMP_DUR_008 | 4_exact… | Clock times / dates |
| PER_POV_001 | first_person if natural else deep third | Consistent person |
| PLT_THM_004 | survival/fear or guilt/redemption | Pressure domain |
| AGENT_ATTR_001 | in-action or in-dialogue first | No long resume open |

## Avoid (model-low for humans on sweeps)
- Opening with external appearance dump only
- Zero aftermath (hard cut at climax)
- Fully open mystery with no turn
- Emotion only as explicit labels (“he was sad”) with no body
```

- [ ] **Step 2: Write `artifacts/human_coding_targets.json`**

```json
{
  "must_hit": {
    "PLT_MOR_007": "extended (multiple scenes/time jumps of aftermath/epilogue)",
    "SIT_MET_303": "4",
    "REV_SUR_007": "climactic_end_twist",
    "EVT_SCH_010": ["frame_confession/memoir"],
    "AGENT_EMO_009": "embodied_sensations_and_metaphors",
    "SIT_MET_008": "Balanced mix of explicit and implicit"
  },
  "support": {
    "TMP_DUR_008": "4_exact_calendar_dates_and_clock_times",
    "PER_POV_001": "first_person",
    "PLT_THM_004": ["survival/fear", "guilt/redemption"]
  }
}
```

- [ ] **Step 3: Commit**

```powershell
cd C:\Users\vstal\noslop
git add skills/noslop/human_coding.md artifacts/human_coding_targets.json
git commit -m "docs: freeze StoryScope human-coding targets for noslop skill"
```

---

### Task 2: Coverage-honest score CLI

**Files:**
- Modify: `src/noslop/score.py`
- Modify: `src/noslop/report.py`
- Modify: `src/noslop/cli.py`
- Create: `tests/test_score_coverage.py`

- [ ] **Step 1: Failing test — sparse features cannot PASS if min_coverage set**

```python
# tests/test_score_coverage.py
from noslop.score import score

def test_sparse_fails_min_coverage():
    r = score(
        features={"SIT_MET_303": "4"},
        model_name="narrative",
        threshold=0.5,
        min_coverage=0.8,
    )
    assert r["coverage"] < 0.8
    assert r["gate"] == "fail"
    assert r.get("warning")
```

- [ ] **Step 2: Run test — expect FAIL (min_coverage missing)**

```powershell
cd C:\Users\vstal\noslop
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m pytest tests/test_score_coverage.py -v
```

Expected: import/error or fail on missing arg.

- [ ] **Step 3: Implement `min_coverage` in `score()`**

In `score.py`, after computing `extracted` / `features_expected`:

```python
coverage = extracted / features_expected if features_expected else 0.0
warning = None
if coverage < 0.8:
    warning = "sparse_features; score may be floor-biased"
gate = "pass" if p_human >= threshold else "fail"
if min_coverage is not None and coverage < min_coverage:
    gate = "fail"
    warning = (warning or "") + f"; coverage {coverage:.2f} < min_coverage {min_coverage}"
```

Add `min_coverage: float | None = None` param; thread from CLI `--min-coverage`.

- [ ] **Step 4: Report coverage in text + JSON**

`report.py`: add `coverage: 0.xx` line.

- [ ] **Step 5: `features-template` subcommand**

```python
# cli: features-template --out template.json [--pack high-gain|core|all]
# dumps {"features": {id: null, ...}} plus "_allowed": {id: values} in sidecar or comments file
```

Minimal: write JSON with all narrative feature IDs as `null`, and a second file `template_allowed.json` mapping id → values list from taxonomy.

- [ ] **Step 6: Tests pass + commit**

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_score_coverage.py -v
git add src/noslop/score.py src/noslop/report.py src/noslop/cli.py tests/test_score_coverage.py
git commit -m "feat: coverage-aware noslop score gate and feature template"
```

---

### Task 3: Rewrite skill for human-coding prompt loop

**Files:**
- Modify: `skills/noslop/SKILL.md`
- Modify: `skills/noslop/checklists.md`
- Modify: `skills/noslop/core_features.md`

- [ ] **Step 1: Replace core pattern in SKILL.md** with:

```text
1. Fill NOSLOP PRE-WRITE (include human-coding plan lines)
2. Draft so human_coding.md targets are visible in the prose
3. Fill features.json (high-gain + core) with cited spans
4. Run: python -m noslop.cli score --features features.json --json
5. If gate FAIL or P(human) < 0.5 → FIX construction (not synonym swaps) → max 2 rounds
6. Ship draft + features + score JSON
```

- [ ] **Step 2: Extend PRE-WRITE template**

```text
NOSLOP PRE-WRITE
Audience:
Length / form:
Specific anchors (name / number / place / time):
Aftermath plan (what happens after climax — required):
End turn / twist (what recontextualizes the piece):
Embodied emotion beat (body + sensation):
Frame device if any (log / later tell / none):
Theme surface (where meaning is allowed to show — not silent):
Rhythm note:
Surface risk:
```

- [ ] **Step 3: GRADE stays structure-focused; add SCORE block**

```text
NOSLOP SCORE
coverage: x.xx
P(human): x.xx
gate: PASS|FAIL
gaps: (feature IDs that should be true in prose but aren't)
FIX: structural bullets targeting gaps
```

- [ ] **Step 4: core_features.md** — list high-gain pack + “cite a span for each fill” rule.

- [ ] **Step 5: Mirror skill to user install paths**

```powershell
Copy-Item -Recurse -Force C:\Users\vstal\noslop\skills\noslop\* $env:USERPROFILE\.claude\skills\noslop\
```

- [ ] **Step 6: Commit**

```powershell
git add skills/noslop/
git commit -m "feat: rewrite noslop skill for StoryScope human-coding loop"
```

---

### Task 4: A/B eval harness + prove mall story

**Files:**
- Create: `evals/prompts.json`
- Create: `evals/run_ab.md`
- Create: `evals/results/` (gitkeep)

- [ ] **Step 1: Write 5 prompts** including the shoe/mall brief.

- [ ] **Step 2: Generate two drafts for mall brief** (agent):
  - default: no skill
  - noslop: full new skill

- [ ] **Step 3: Fill features for both** using high-gain+core with **span citations** in a side file `features_*_cites.md`.

- [ ] **Step 4: Score both**

```powershell
cd C:\Users\vstal\noslop
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m noslop.cli score --features evals/results/mall_noslop_features.json --json
.\.venv\Scripts\python.exe -m noslop.cli score --features evals/results/mall_default_features.json --json
```

- [ ] **Step 5: Pass criteria check**

- noslop P(human) ≥ default + 0.15  
- If not, revise skill recipe (Task 3) and re-run once.

- [ ] **Step 6: Commit results table in `evals/results/SUMMARY.md`**

```powershell
git add evals/
git commit -m "test: A/B eval showing noslop lifts StoryScope P(human)"
```

---

### Task 5: README + install one-liner

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Document**

```powershell
# score a filled map
$env:PYTHONPATH="src"
python -m noslop.cli score --features features.json --json --min-coverage 0.5

# template for agent fill
python -m noslop.cli features-template --pack high-gain --out features_template.json
```

Skill flow: PRE-WRITE → draft → fill → score → FIX.

- [ ] **Step 2: Commit**

```powershell
git add README.md
git commit -m "docs: noslop human-coding score loop usage"
```

---

## Self-review

| Spec requirement | Task |
|------------------|------|
| Skill targets human-coding constructions | Task 1, 3 |
| Honest feature fill + coverage | Task 2, 3 |
| Score loop | Task 3 |
| A/B proof | Task 4 |
| Docs | Task 5 |
| No forged features without prose | Task 3 cites rule + Task 4 cites file |

No TBD placeholders in steps above.

---

## Execution handoff

Plan saved to `docs/superpowers/plans/2026-07-15-noslop-score-human.md`.

**1. Subagent-Driven (recommended)** — fresh subagent per task  
**2. Inline Execution** — one session with checkpoints  

Or paste the `/goal` prompt below to run autonomously.
