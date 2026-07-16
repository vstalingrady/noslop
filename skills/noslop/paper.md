# StoryScope (paper notes)

Russell et al., *StoryScope: Investigating idiosyncrasies in AI fiction*  
arXiv: [2604.03136](https://arxiv.org/abs/2604.03136) · code: [jenna-russell/storyscope](https://github.com/jenna-russell/storyscope)

## Claim

AI fiction and human fiction can differ in **how the story is built** (discourse / construction), not only in surface style (word choice, glue phrases).

Corpus: parallel ~**5,000-word** stories from the same prompts. Features were **extracted from text**, then classified.

## AI tends to

- **Over-explain themes** — narrator states the moral; dialogue as philosophy seminar
- **Tidy single-track plots** — tight causal chains, fewer subplots, closed resolution
- **Formulaic “show don’t tell”** — body/senses defaults; setting mirrors mood on rails
- **Cluster** — models sit in a shared region of narrative space

## Humans tend to

- **Moral ambiguity** — greyer choices; messier costs
- **Temporal complexity** — flashbacks, jumps, delayed revelation when the form allows
- **Specific outside world** — names, places, cultural detail
- **More diversity** — rarer combinations of narrative decisions

## How noslop uses this

| Form | Apply |
|------|--------|
| **Long fiction** (~1k+ words) | Less theme dump; greyer choices; time texture when length allows; avoid single-track tidy lesson |
| **Short agent prose** | Flow + anti-glue + real anchors — leave novel discourse toys out |

| Ship | Lab |
|------|-----|
| Readable page finishes | StoryScope CLI / feature packs when asked |
| VOICE hard fails (sermon / ban spam) | Honest feature labels only — never forge |
| Balanced mode default | Book-band scores (~0.1–0.3 P(human)) are fine when the page flows |

Ban lists clean surface noise. Construction and flow carry the writing.
