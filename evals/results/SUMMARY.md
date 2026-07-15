# noslop A/B StoryScope score SUMMARY

Scorer: `python -m noslop.cli score --features ... --json` with repo venv + `PYTHONPATH=src`.
Model: `binary_narrative` (weights unchanged).
Honesty: each feature value has a draft span in `*_cites.md`.

## Per-brief results

| Brief | default P(human) | noslop P(human) | delta | default cov | noslop cov | delta>=0.15? | noslop>=0.5? |
|-------|------------------|-----------------|-------|-------------|------------|--------------|--------------|
| mall_shoe | 0.0264 | 0.7118 | +0.6854 | 0.087 (23/265) | 0.087 (23/265) | YES | YES |
| cold_email | 0.0236 | 0.5252 | +0.5016 | 0.075 (20/265) | 0.087 (23/265) | YES | YES |
| personal_bio | 0.0239 | 0.5868 | +0.5628 | 0.072 (19/265) | 0.087 (23/265) | YES | YES |
| saas_blurb | 0.0236 | 0.5293 | +0.5057 | 0.068 (18/265) | 0.087 (23/265) | YES | YES |
| agent_answer | 0.0236 | 0.5405 | +0.5170 | 0.068 (18/265) | 0.087 (23/265) | YES | YES |

## Criteria (vs default AI only)
- A/B delta >= 0.15 on >=4/5: **5/5** -> **PASS**
- Absolute noslop P(human) >= 0.5 on >=3/5: **5/5** -> **PASS**

## Human book baseline (NOT the same as “sounds literary”)

See `evals/results/HUMAN_BASELINE.md`.

| Cohort | mean P(human) | mean P(AI) ≈ slop |
|--------|---------------|-------------------|
| Book excerpts (5 honest maps) | **0.128** | **0.872** |
| default AI (5) | 0.024 | 0.976 |
| noslop AI (5) | **0.579** | **0.421** |

**Finding:** On this scorer, **classic human prose looks more like “AI/slop” than noslop-engineered AI.** Hemingway ~0.03 P(human); Gatsby best human ~0.27; noslop mean ~0.58.

**Implication:** StoryScope PASS is **not** “as human as books.” It is “matches the model’s human-class feature recipe.” Forced must-hit labels on book maps jump them to ~0.56–0.70 (gaming). **Literary / reader-slop job is not done** if that is the bar.

## Honesty notes (skeptic fixes)
- PLT_MOR_007=extended only where draft has multiple post-climax scenes/time-jumps (not career-arc or one coda paragraph).
- saas/bio/agent/cold noslop drafts expanded with explicit multi-beat aftermath after climax.
- agent_answer: SIT_MET_104 = generic_second_person; features are per-draft maps with cites.

## Paths

| Brief | Arm | Draft | Features | Cites | Score JSON |
|-------|-----|-------|----------|-------|------------|
| mall_shoe | default | `evals/results/mall_shoe_default.md` | `evals/results/mall_shoe_default_features.json` | `evals/results/mall_shoe_default_cites.md` | `evals/results/mall_shoe_default_score.json` |
| mall_shoe | noslop | `evals/results/mall_shoe_noslop.md` | `evals/results/mall_shoe_noslop_features.json` | `evals/results/mall_shoe_noslop_cites.md` | `evals/results/mall_shoe_noslop_score.json` |
| cold_email | default | `evals/results/cold_email_default.md` | `evals/results/cold_email_default_features.json` | `evals/results/cold_email_default_cites.md` | `evals/results/cold_email_default_score.json` |
| cold_email | noslop | `evals/results/cold_email_noslop.md` | `evals/results/cold_email_noslop_features.json` | `evals/results/cold_email_noslop_cites.md` | `evals/results/cold_email_noslop_score.json` |
| personal_bio | default | `evals/results/personal_bio_default.md` | `evals/results/personal_bio_default_features.json` | `evals/results/personal_bio_default_cites.md` | `evals/results/personal_bio_default_score.json` |
| personal_bio | noslop | `evals/results/personal_bio_noslop.md` | `evals/results/personal_bio_noslop_features.json` | `evals/results/personal_bio_noslop_cites.md` | `evals/results/personal_bio_noslop_score.json` |
| saas_blurb | default | `evals/results/saas_blurb_default.md` | `evals/results/saas_blurb_default_features.json` | `evals/results/saas_blurb_default_cites.md` | `evals/results/saas_blurb_default_score.json` |
| saas_blurb | noslop | `evals/results/saas_blurb_noslop.md` | `evals/results/saas_blurb_noslop_features.json` | `evals/results/saas_blurb_noslop_cites.md` | `evals/results/saas_blurb_noslop_score.json` |
| agent_answer | default | `evals/results/agent_answer_default.md` | `evals/results/agent_answer_default_features.json` | `evals/results/agent_answer_default_cites.md` | `evals/results/agent_answer_default_score.json` |
| agent_answer | noslop | `evals/results/agent_answer_noslop.md` | `evals/results/agent_answer_noslop_features.json` | `evals/results/agent_answer_noslop_cites.md` | `evals/results/agent_answer_noslop_score.json` |

## Skill install
Mirrored to `%USERPROFILE%\.claude\skills\noslop\`.

## Tests
`tests/test_score_coverage.py` — coverage + features-template.

