# noslop v2 VOICE A/B SUMMARY

Primary gate: `python -m noslop.cli voice` (threshold 6.5, no hard_fail).
StoryScope P(human) is **not** the ship gate. Books mean ~0.13 — see HUMAN_BASELINE.md.
GPTZero: not run in this environment (optional; no undetectable claim).

## Per-brief

| Brief | default | noslop-v2 | delta | noslop>=6.5? | delta>=1.5? |
|-------|---------|-----------|-------|--------------|-------------|
| mall_shoe | 0.88 (fail) | 9.12 (pass) | +8.24 | YES | YES |
| cold_email | 4.91 (fail) | 9.12 (pass) | +4.21 | YES | YES |
| personal_bio | 3.16 (fail) | 9.12 (pass) | +5.96 | YES | YES |
| saas_blurb | 3.16 (fail) | 8.25 (pass) | +5.09 | YES | YES |
| agent_answer | 5.26 (fail) | 8.25 (pass) | +2.99 | YES | YES |

## Criteria
- noslop VOICE >= 6.5 and delta >= 1.5 on >=4/5: **5/5** -> **PASS**

## Paths

| Brief | Arm | Draft | Voice JSON |
|-------|-----|-------|------------|
| mall_shoe | default | `evals/results/v2/mall_shoe_default.md` | `evals/results/v2/mall_shoe_default_voice.json` |
| mall_shoe | noslop | `evals/results/v2/mall_shoe_noslop.md` | `evals/results/v2/mall_shoe_noslop_voice.json` |
| cold_email | default | `evals/results/v2/cold_email_default.md` | `evals/results/v2/cold_email_default_voice.json` |
| cold_email | noslop | `evals/results/v2/cold_email_noslop.md` | `evals/results/v2/cold_email_noslop_voice.json` |
| personal_bio | default | `evals/results/v2/personal_bio_default.md` | `evals/results/v2/personal_bio_default_voice.json` |
| personal_bio | noslop | `evals/results/v2/personal_bio_noslop.md` | `evals/results/v2/personal_bio_noslop_voice.json` |
| saas_blurb | default | `evals/results/v2/saas_blurb_default.md` | `evals/results/v2/saas_blurb_default_voice.json` |
| saas_blurb | noslop | `evals/results/v2/saas_blurb_noslop.md` | `evals/results/v2/saas_blurb_noslop_voice.json` |
| agent_answer | default | `evals/results/v2/agent_answer_default.md` | `evals/results/v2/agent_answer_default_voice.json` |
| agent_answer | noslop | `evals/results/v2/agent_answer_noslop.md` | `evals/results/v2/agent_answer_noslop_voice.json` |

## Flagship
`evals/results/v2/sample_flagship.md` (same brief as mall_shoe noslop arm).

## Skill
VOICE primary in `skills/noslop/SKILL.md`; mirrored to `%USERPROFILE%\.claude\skills\noslop\`.
XGBoost model not retrained.

## Figures

Run `python evals/plot_compare.py` → `evals/results/figures/`
(bar chart, deltas, axis heatmap, excerpt panels, optional StoryScope/books).

