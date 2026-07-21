# Longform samples

StoryScope’s paper corpus used ~**5,000-word** parallel stories (Russell et al., arXiv:2604.03136).  
Short modes under `evals/results/modes/` stay short on purpose. Construction shows up at length.

**How to judge:** read the page. Do **not** use VOICE or StoryScope P(human) as the win. Prefer the draft a careful human finishes without template nausea (grey cost, no TED close, not a single-track acceptance bow).

Skill method for new long fiction: [skills/noslop/construction.md](../../../skills/noslop/construction.md) — PRE-STRUCTURE → sparse **2–4** moves → diversity seed → structural FIX → polish last.
Skill method for long nonfiction: [skills/noslop/structure-nonfiction.md](../../../skills/noslop/structure-nonfiction.md) — PRE-DRAFT → **2–4** palette picks + macro seed (order / omissions / stopping points) → named skips → one structural re-pass max.

| File | Role |
|------|------|
| [`c7_paper_aligned.md`](c7_paper_aligned.md) | Sparse-ish construction lean: greyer choice, temporal texture, no TED close |
| [`c7_ai_construction.md`](c7_ai_construction.md) | Same premise, AI defaults: theme over-explain, tidy single-track, lesson close |
| [`c8_default.md`](c8_default.md) | c8 control: raw model, **no skill, no tools**, same brief. Overran the 1k brief (~1.4k) and kept its template skeleton — both left as-is; that's what default does |
| [`c8_nonfiction.md`](c8_nonfiction.md) | c8 treatment: skill + structure-nonfiction.md, ~1k words |

**c8 note:** first nonfiction pair, ~1,000-word brief ("an essay about poop"). Both arms written by fresh-context agents — the planner had seen a detector report on an earlier draft, so its own rewrite would have been fitted to the detector and proved nothing. Any detector score on these files is a footnote, not the win; the win is which draft a careful human finishes.

**Diversity seed note:** two drafts of the same brief should pick different unused moves so they are not twins. Full multi-seed twin proof is optional evidence; the method lives in the skill.

Word count:

```powershell
(Get-Content evals\results\longform\c7_paper_aligned.md -Raw).Split(
  [char[]]@(' ','`n','`r','`t'), 'RemoveEmptyEntries'
).Count
```
