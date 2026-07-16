# Longform samples

StoryScope’s paper corpus used ~**5,000-word** parallel stories (Russell et al., arXiv:2604.03136).  
Short modes under `evals/results/modes/` stay short on purpose. Construction shows up at length.

| File | Role |
|------|------|
| [`c7_paper_aligned.md`](c7_paper_aligned.md) | Long fiction: greyer choice, temporal texture, no TED close |
| [`c7_ai_construction.md`](c7_ai_construction.md) | Same premise, AI defaults: theme over-explain, tidy single-track |

Word count:

```powershell
(Get-Content evals\results\longform\c7_paper_aligned.md -Raw).Split(
  [char[]]@(' ','`n','`r','`t'), 'RemoveEmptyEntries'
).Count
```
