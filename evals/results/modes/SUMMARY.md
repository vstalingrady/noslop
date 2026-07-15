# noslop modes — flow over score (paper realign)

StoryScope (arXiv:2604.03136) measured **discourse construction** on fiction,
not “maximize this VOICE number.” Ship bar = careful human finishes the page.

Scored with `noslop.voice.score_voice` / CLI voice path as **soft anti-glue only**.
VOICE numbers are **not** a flow ranking. Read the drafts.
StoryScope binary not run here (no forged features).

## Scores (informative only)

| Brief | default | modest | balanced | max |
|-------|---------|--------|----------|-----|
| mall_shoe | 0.88 | 8.07 | 8.25 | 7.19 |
| cold_email | 4.91 | 10.00 | 9.12 | 8.07 |

## Gates (hard_fail)

| Brief | default | modest | balanced | max |
|-------|---------|--------|----------|-----|
| mall_shoe | HARD | pass | pass | pass |
| cold_email | HARD | pass | pass | pass |

## Human-flow notes (primary judge)

- **modest** — unforced; digression OK; fewest craft stamps.
- **balanced** — **ship default**; readable; anti-glue/sermon; no arc-toy dump.
- **max** — research only: frame/turn/aftermath stamps on purpose; stiffer; **not** product win even if VOICE is high.
- **default** — control slop (glue + sermon).

## Recommendation

- **Ship: balanced.**
- **modest** for natural letters / low pressure.
- **max** only when labeled research / stress craft.
- High VOICE + stiff craft = failure. Book-band StoryScope (~0.1–0.3) OK when flow is good.
- Longform StoryScope illustration: **skipped** this cycle (optional; not ship bar).

## Drafts

- `mall_shoe_default.md`
- `mall_shoe_modest.md`
- `mall_shoe_balanced.md`
- `mall_shoe_max.md`
- `cold_email_default.md`
- `cold_email_modest.md`
- `cold_email_balanced.md`
- `cold_email_max.md`
