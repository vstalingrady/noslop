# noslop: Make AI Text Score Human (StoryScope)

**Date:** 2026-07-15  
**Goal:** Clever prompting (the noslop skill) so AI-written text is *constructed* like human narrative and the local XGBoost StoryScope scorer reports higher **P(human)** — ideally gate PASS (≥0.5).

## What we learned

Scorer is `artifacts/models/noslop_binary_narrative.json` (StoryScope-style discourse features → P(human)).

Empty feature map → P(human) ≈ **0.038**. Sparse fills of “anti-slop” drafts (open ending, low moralizing) stayed ~0.02–0.09 FAIL.

**Single-feature lifts vs empty** (host sweep on high-gain IDs):

| Feature | Human-pushing value | Δ P(human) alone |
|---------|---------------------|------------------|
| `PLT_MOR_007` | extended aftermath / epilogue | **+0.13** |
| `SIT_MET_303` | thematic explicitness **4** | **+0.11** |
| `REV_SUR_007` | climactic end twist | **+0.10** |
| `EVT_SCH_010` | frame_confession/memoir | +0.04 |
| `AGENT_EMO_009` | embodied_sensations_and_metaphors | +0.02 |
| `SIT_MET_008` | balanced explicit+implicit refs | +0.02 |

**Stack of 8 best high-gain values** → P(human) ≈ **0.79** (PASS) — proof the model *can* fire human when features align.

**Implication:** old skill optimized “anti-slop taste” (no moral close, open thread, low sermon). That **fights** this model. New skill must optimize **human-coding construction** that (1) lives in the actual prose and (2) is labeled honestly in `features.json`.

Not allowed: forge feature JSON while the draft lacks those properties. Allowed: prompt the model to *write* so those properties are true.

## Success criteria

1. **A/B:** same brief, noslop skill vs default → noslop **P(human) ≥ default + 0.15** on ≥4/5 prompts.
2. **Absolute:** noslop arm **P(human) ≥ 0.5** (gate PASS) on ≥3/5 prompts with **≥80% feature coverage** (extracted/expected).
3. **Honesty:** feature map filled from the draft (rubric / LLM extract), not hand-picked to max score without reading.
4. **Skill-only path:** an agent with only `skills/noslop/*` + CLI can run PRE-WRITE → draft → feature fill → score → FIX loop without this design doc.

## Architecture

```
                    ┌─────────────────────┐
  brief ──────────►│ noslop skill (prompt)│
                    │ PRE-WRITE targets    │
                    │ human-coding recipe  │
                    └──────────┬──────────┘
                               ▼
                            draft.md
                               │
              ┌────────────────┼────────────────┐
              ▼                                 ▼
     fill features.json                  (optional surface polish)
     (agent rubric or LLM extract         style-and-bans.md
      over taxonomy / core+high-gain)
              │
              ▼
     python -m noslop.cli score --features ... --json
              │
         P(human) gate
              │
         FAIL → structural FIX from score gaps → re-draft (max 2)
         PASS → ship draft + features + score report
```

### Three layers

1. **Skill (prompt engineering)** — rewrite PRE-WRITE / draft recipe / GRADE so drafts *enact* human-coding targets (see below).
2. **Feature fill** — reliable map with high coverage (≥80% of narrative IDs, or at least all high-gain IDs + core set).
3. **Score loop** — CLI gate; FIX instructions map failed / low features → prose changes.

### Human-coding recipe (prompt targets)

Skill must instruct the writer to build:

| Construction in prose | Feature target |
|----------------------|----------------|
| After the climax, stay for aftermath (second scene, time jump, what changed next week) | `PLT_MOR_007` = extended |
| Theme/meaning surfaces in character thought or one clear line (not zero, not pure sermon spam) — aim moderate-high explicitness | `SIT_MET_303` ≈ 3–4 |
| A real turn near the end that recontextualizes the shoe/object/choice | `REV_SUR_007` = climactic_end_twist |
| Voice with body/sensation (throat, cold tile, weight in hand) not only “he felt sad” | `AGENT_EMO_009` = embodied |
| Optional frame: log entry, later recollection, “I’m writing this after…” | `EVT_SCH_010` includes frame_confession/memoir |
| Concrete anchors + one cultural/local echo (song, brand, local myth) not empty | `SIT_MET_008` balanced or implicit echoes |
| First person *or* deep third with free indirect style where natural | `PER_POV_001` / monologue channels |
| Survival/fear or coming-of-age pressure when genre fits | `PLT_THM_004` / `PLT_THM_006` |

Still keep: specific names/times/places (`TMP_DUR_008` precision), varied sentence rhythm, ban-list surface polish *after* structure.

**Drop or soften as primary goals:** “leave mystery fully open,” “never state theme,” “no denouement” — those tank this scorer.

### Feature fill strategy (v1)

Priority order:

1. **High-gain pack** (~25 IDs from model gain) — must always fill.
2. **core_features.md** (19) — always fill.
3. **Expand** toward 265 via checklist templates per dimension (agents fill N/A-safe defaults for short text).

CLI changes:

- Report `coverage`; if coverage < 0.8 → `warning: sparse; score may be floor-biased` (already partly true).
- Add `score --min-coverage 0.8` that refuses PASS when sparse (honest gate).
- Optional: `noslop.cli features-template` dumps empty JSON of all narrative IDs + allowed values for agent fill.

### Eval harness

`evals/prompts.json` — 5 briefs.  
Script: generate default vs noslop (or use stored drafts) → fill features → score → table.

Ship criterion for skill change: A/B pass rates above success criteria.

## Non-goals (v1)

- Retraining XGBoost on new labels.
- Pure ban-list “deslop” as primary metric.
- Gaming JSON without matching prose.

## Risks

| Risk | Mitigation |
|------|------------|
| Skill becomes “write like the paper’s human class” not “nice prose” | Keep surface bans + anchors; human spot-check samples |
| Agents fill features optimistically | Rubric: each filled ID needs a cited span in draft |
| 265-fill too heavy | v1 = high-gain + core (~40); prove lift; then expand |
| Genre mismatch (email vs fiction) | Genre branch in PRE-WRITE; nonfiction maps extended close → “callback + consequence paragraph” |

## Done when

Mall-shoe A/B re-run: noslop P(human) clearly above default and preferably ≥0.5 with coverage ≥0.8; skill docs match recipe; one README command reproduces score.
