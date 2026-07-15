# StoryScope (what the paper measured)

Russell et al., *StoryScope: Investigating idiosyncrasies in AI fiction*  
arXiv: [2604.03136](https://arxiv.org/abs/2604.03136) · code: [jenna-russell/storyscope](https://github.com/jenna-russell/storyscope)

Read this before treating any noslop score as “write better.”

## One claim

AI fiction and human fiction can differ in **how the story is built** (discourse / construction), not only in surface style (word choice, glue phrases).

Paper corpus: parallel ~**5,000-word** stories from the same prompts. Features were **extracted from text**, then classified — not hand-forged to raise a score.

## What AI tends to do (paper)

- **Over-explain themes** — narrator states the moral; dialogue as philosophy seminar
- **Tidy single-track plots** — tight causal chains, fewer subplots, closed resolution
- **Formulaic “show don’t tell”** — emotion via body/senses defaults; setting mirrors mood on rails
- **Cluster** — models sit in a shared region of narrative space (less diversity)

## What humans tend to do (paper)

- **Moral ambiguity** — greyer protagonist choices; messier costs
- **Temporal complexity** — flashbacks, jumps, delayed revelation when the form allows
- **Specific outside world** — named references, reader address, cultural place
- **More diversity** — rarer combinations of narrative decisions

## What this is not

| Paper | Not the paper |
|-------|----------------|
| Construction on long fiction | Ban-list as the whole skill |
| Detector / description research | “Maximize P(human)” writing coach |
| Honest feature extraction | Forge feature JSON to game the binary |
| Book-band scores can still be good writing | Ship only if P(human) ≥ 0.5 |

## Genre rule for noslop

| Form | Use from the paper |
|------|--------------------|
| **Long fiction** (~1k+ words, stories/chapters) | Less theme dump; greyer choices; time texture when length allows; avoid single-track tidy lesson |
| **Short agent prose** (email, bio, blurb, Q&A) | Flow + anti-glue + real anchors — **do not** force novel toys (aftermath arcs, frame/memoir, theme scales) |

## Lab vs ship

- **Ship bar:** a careful human finishes the page without fatigue or “this is a template” nausea.
- **StoryScope CLI / feature packs:** lab only. Never the ship gate. Never forge. Never require P(human) ≥ 0.5.
- **VOICE:** soft anti-glue (hard fails for sermon/ban spam). Not “human quality.” Not maximize-to-9+.

Books on the local StoryScope scorer often land ~**0.13–0.27** P(human) and still read fine. Sky-high scores with stiff craft = failure.
