# Human book baseline vs noslop / default (StoryScope)

**Question:** How do real human book excerpts score vs our AI arms on the same XGBoost StoryScope scorer?

**Slop proxy here:** `P(AI) = 1 - P(human)` (higher = more “AI/slop” according to the model).

## Results (honest feature maps from prose)

| Source | P(human) | P(AI) ≈ slop | gate |
|--------|----------|--------------|------|
| Hemingway, *A Farewell to Arms* (open) | **0.029** | **0.971** | fail |
| McCarthy, *The Road* (excerpt) | **0.062** | **0.938** | fail |
| Woolf, *To the Lighthouse* (open) | **0.119** | **0.881** | fail |
| Austen, *Pride and Prejudice* (open) | **0.165** | **0.835** | fail |
| Fitzgerald, *Gatsby* (open) | **0.267** | **0.733** | fail |
| **MEAN human** | **0.128** | **0.872** | — |
| MEAN default AI | 0.024 | 0.976 | fail |
| MEAN noslop AI | **0.579** | **0.421** | mostly pass |

Artifacts: `evals/results/human/*_features.json`, `*_score.json`, drafts with source lines.

## Gaming check

Forcing the noslop **must-hit** feature pack onto human maps (labels the books do **not** all support) jumps them into noslop range:

| Human | honest P(human) | + forced must-hit |
|-------|-----------------|-------------------|
| Hemingway | 0.029 | 0.565 |
| Woolf | 0.119 | 0.697 |
| Gatsby | 0.267 | 0.611 |

**Must-hit stack alone (no draft):** P(human) ≈ **0.715**.

So the scorer rewards a **feature recipe** (extended aftermath + theme 3–4 + end twist + memoir frame + embodied…), not “sounds like a published novel.”

## Interpretation

1. **Default AI** ≈ bottom (highest slop). Skill still wins vs default.
2. **Classic human prose** scores **worse** than noslop on this model (higher P(AI)).
3. Therefore **P(human) ≥ 0.5 is not “as good as books.”** It is “matches the model’s human-class construction template,” which many great books do not use (Hemingway: low theme, no twist, no extended denouement).
4. If the product goal is **“like books / less slop to a reader,”** StoryScope-only PASS is **not done**.
5. If the product goal is only **“beat default AI on StoryScope,”** that bar is met — but the human baseline falsifies reading PASS as literary human-ness.

## What “done” should mean next

| Goal | Metric |
|------|--------|
| Beat AI slop baseline | noslop P(human) ≥ default + 0.15 (current eval) |
| Match books | **Cannot** use raw P(human)≥0.5; need human-panel, dual gate, or a model trained on literary vs slop labels |
| Anti-game | Cap overfit: e.g. require constructions also attested in high-scoring *honest human* samples (Gatsby-like frame+theme) without stacking unsupported extended/twist |

## Sources (excerpts)

- Hemingway, *A Farewell to Arms* (1929) — US PD
- Woolf, *To the Lighthouse* (1927) — US PD  
- Fitzgerald, *The Great Gatsby* (1925) — US PD
- Austen, *Pride and Prejudice* (1813) — PD
- McCarthy, *The Road* (2006) — short fair-use eval excerpt only
