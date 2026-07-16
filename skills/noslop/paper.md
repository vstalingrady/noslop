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

## Do not invert the detector into a generator

StoryScope is a **research detector / description** tool — not a writing coach that says “maximize P(human).”

- A **must-hit** stack of every human-leaning feature creates a **new cluster** (still model-made).
- Use **sparse** selection (2–4 moves) + a **diversity seed** (deliberately unused moves). See [construction.md](construction.md).
- Features should be **extracted** from real text with span cites — never forged to raise a score.
- Style polish alone barely changes narrative detection; **structure** must change on the page.
- Book-band scores (~0.1–0.3 P(human)) with honest labels are fine when the page flows.

## How noslop uses this

| Form | Apply |
|------|--------|
| **Long fiction** (~1k+ words) | PRE-STRUCTURE → sparse 2–4 moves → draft → structural FIX → polish ([construction.md](construction.md)) |
| **Short agent prose** | Flow + anti-glue + real anchors — leave novel discourse toys out |

| Ship | Lab |
|------|-----|
| Careful reader finishes the page | StoryScope CLI / feature packs when asked |
| VOICE hard fails (sermon / ban spam) as anti-glue floor only | Honest feature labels only — never forge |
| Balanced mode default; sparse construction | Book-band scores fine when page flows |
| Score-max + stiff craft = FAIL | Never sole ship gate |

Ban lists clean surface noise. Construction and flow carry the writing. High VOICE or high P(human) is **not** “more human.”
