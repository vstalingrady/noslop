# VOICE A/B summary

Primary check: `python -m noslop.cli voice` (soft anti-glue; hard fails block).  
StoryScope is lab-only — see [`HUMAN_BASELINE.md`](HUMAN_BASELINE.md).

## Per-brief

| Brief | default | noslop | delta |
|-------|---------|--------|-------|
| mall_shoe | 0.88 | 9.12 | +8.24 |
| cold_email | 4.91 | 9.12 | +4.21 |
| personal_bio | 3.16 | 9.12 | +5.96 |
| saas_blurb | 3.16 | 8.25 | +5.09 |
| agent_answer | 5.26 | 8.25 | +2.99 |

All five: noslop clears hard fail and lifts vs default.

## Paths

| Brief | default draft | noslop draft |
|-------|---------------|--------------|
| mall_shoe | `v2/mall_shoe_default.md` | `v2/mall_shoe_noslop.md` |
| cold_email | `v2/cold_email_default.md` | `v2/cold_email_noslop.md` |
| personal_bio | `v2/personal_bio_default.md` | `v2/personal_bio_noslop.md` |
| saas_blurb | `v2/saas_blurb_default.md` | `v2/saas_blurb_noslop.md` |
| agent_answer | `v2/agent_answer_default.md` | `v2/agent_answer_noslop.md` |

Flagship sample: `v2/sample_flagship.md`  
Skill: [`skills/noslop/`](../../skills/noslop/)  
Figures: `python evals/plot_compare.py` → `figures/`
