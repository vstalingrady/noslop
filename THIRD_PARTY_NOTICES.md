# Third-party notices

## StoryScope

Taxonomy design and research basis:

**StoryScope: Investigating idiosyncrasies in AI fiction**  
Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting  
arXiv: [2604.03136](https://arxiv.org/abs/2604.03136)  
Code: [github.com/jenna-russell/storyscope](https://github.com/jenna-russell/storyscope)

License: MIT — Copyright (c) 2026 Jenna Russell

noslop includes `artifacts/taxonomy.json` and trained weights under
`artifacts/models/noslop_binary_*.json` for local scoring.

## Surface ban / pattern lists (adapted)

noslop’s `skills/noslop/style-and-bans.md` surface vocabulary, phrase bans,
punctuation budgets, and self-check patterns are adapted in part from open
anti-slop writing skills and public AI-tell compilations, including:

**anti-ai-slop-writing**  
[github.com/jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing)  
License: MIT

noslop is **not** a fork of that skill. StoryScope construction, PRE-STRUCTURE,
diversity seeds, modes, VOICE scoring, and the “page judgment over scoremax”
ship bar are noslop-specific. Surface lists are reorganized, trimmed, and
paired with construction so neither pillar stands alone.
