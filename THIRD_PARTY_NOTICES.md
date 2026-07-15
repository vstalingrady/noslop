# Third-party notices

## StoryScope

This project uses code, taxonomy, and trained model weights from:

**StoryScope: Investigating idiosyncrasies in AI fiction**  
Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting  
arXiv: [2604.03136](https://arxiv.org/abs/2604.03136)  
Code: [github.com/jenna-russell/storyscope](https://github.com/jenna-russell/storyscope)

License: MIT License  
Copyright (c) 2026 Jenna Russell

See `third_party/storyscope/LICENSE` for the full text.

What we use:

- Feature taxonomy (`taxonomy.json`)
- Feature application prompts and extraction logic
- Released XGBoost weights (`binary_narrative.json`, `binary_full.json`, …)
- Feature encoder utilities

noslop adds a single-document inference CLI and an agent skill. We do not retrain the paper models by default.
