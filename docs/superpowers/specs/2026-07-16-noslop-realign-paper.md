# noslop realign — back to StoryScope’s actual plot

**Date:** 2026-07-16  
**Status:** design / goal handoff  
**Paper:** Russell et al., *StoryScope: Investigating idiosyncrasies in AI fiction*  
arXiv: [2604.03136](https://arxiv.org/abs/2604.03136) · [code](https://github.com/jenna-russell/storyscope)

## What the paper is (do not reverse)

| Paper | Not the paper |
|-------|----------------|
| Discourse-level **narrative construction** | Surface style as the main story |
| Long fiction (~**5k words**/story in corpus) | 100-word email score farming |
| Features **extracted from text**, then classify | Forge feature JSON to raise P(human) |
| AI: **over-explains themes**, **tidy single-track plots** | “Hit VOICE 9.1 / P(human) 0.7” |
| Human: **moral ambiguity**, **temporal complexity**, **more diversity** in narrative space | One optimized recipe for every genre |
| Research **detection / description** | Product “undetectable” marketing |

Quote-level finding (abstract): narrative features alone separate human vs AI well; AI stories cluster; humans are more diverse. Compact signal includes theme over-explanation and tidy plots vs ambiguous choices and messier time.

## How noslop lost the plot

1. Treated StoryScope binary as a **writing coach** that says “go max.”  
2. Hand-labeled features without paper-style extraction → **forgery works**.  
3. Applied novel-length discourse metrics to **short agent outputs**.  
4. Layered **VOICE checklists** that became a new template (staccato, even craft).  
5. Declared victory on **numbers** while the page stayed unreadable.

## Realignment principle

**Ship bar = a careful human finishes the page without fatigue or “this is a template” nausea.**

- Surface hygiene stays (no glue spam, no sermon close).  
- **Paper-aligned construction** for fiction: less theme lecture, greyer choices, more temporal texture when length allows, **avoid single-track tidy resolution**.  
- **Diversity**: no one winning pack for every brief.  
- StoryScope: **lab instrument** for long fiction analysis — not the ship gate.  
- Book-band StoryScope (~0.1–0.3) with honest labels is **not failure**. Sky-high scores with stiff prose **are**.  
- Modes (modest / balanced / max) stay: **balanced** ship default; **max** = research only.

## Genre split (critical)

| Form | Primary rules |
|------|----------------|
| **Long fiction** | Paper construction (ambiguity, time, no theme dump, multi-track OK) + flow |
| **Short agent prose** (email, bio, blurb, answers) | Flow + anti-glue + anchors when natural — **do not** force novel discourse toys |
| **StoryScope score** | Only for long-form or explicit research; honest extract/label; never forge |

## Success criteria (realign)

1. Skill rewritten around **paper findings + human flow**; score-max language removed from ship path.  
2. Modes kept; balanced = default; max labeled research.  
3. Eval: same brief across modes — **primary judge is human-readable drafts**, VOICE only as soft anti-glue; optional StoryScope only on longer fiction samples if any.  
4. DOCX or refresh of modes report: states paper thesis, shows modest/balanced/max side-by-side, recommends **balanced**, warns against max-as-product.  
5. README: plain English; paper cited as **what StoryScope measured**; install at bottom; no detector-failure theater.  
6. Commit + push.  
7. No XGBoost retrain this cycle.

## Non-goals

- Guaranteed commercial detector pass  
- Forcing StoryScope P(human) ≥ 0.5  
- Deleting VOICE CLI (still useful vs pure glue)  
- Full reimplementation of StoryScope extraction pipeline (optional later)

## Later (out of this goal)

- LLM-assisted **honest** feature application on 2k+ word fiction only  
- Diversity metrics across drafts (anti-clustering)  
- Reader panel / preference A/B
