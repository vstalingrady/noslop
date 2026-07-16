# Longform samples

StoryScope’s paper corpus used ~**5,000-word** parallel stories (Russell et al., arXiv:2604.03136).  
Short modes under `evals/results/modes/` stay short on purpose. Construction shows up at length.

**How to judge:** read the page. Do **not** use VOICE or StoryScope P(human) as the win. Prefer the draft a careful human finishes without template nausea (grey cost, no TED close, not a single-track acceptance bow).

Skill method for new long fiction: [skills/noslop/construction.md](../../../skills/noslop/construction.md) — PRE-STRUCTURE → sparse **2–4** moves → diversity seed → structural FIX → polish last.

| File | Role |
|------|------|
| [`c7_paper_aligned.md`](c7_paper_aligned.md) | Sparse-ish construction lean: greyer choice, temporal texture, no TED close |
| [`c7_ai_construction.md`](c7_ai_construction.md) | Same premise, AI defaults: theme over-explain, tidy single-track, lesson close |

**Diversity seed note:** two drafts of the same brief should pick different unused moves so they are not twins. Full multi-seed twin proof is optional evidence; the method lives in the skill.

Word count:

```powershell
(Get-Content evals\results\longform\c7_paper_aligned.md -Raw).Split(
  [char[]]@(' ','`n','`r','`t'), 'RemoveEmptyEntries'
).Count
```
