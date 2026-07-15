---
name: noslop
description: >-
  Use when drafting or rewriting prose that must sound human (articles, emails,
  stories, bios, reports, long agent answers), or when the user says noslop,
  anti AI voice, write human, or /noslop. Gates delivery with the StoryScope
  paper scorer. Not for code cleanup.
---

# noslop

Write first. Prove it with StoryScope. No vibes-only “I checked.”

## What this is

- **Writing rules** — short construction habits that fight AI monotony  
- **Gate** — `noslop score` runs the **StoryScope** detector from Russell et al. (arXiv:2604.03136): discourse features → released XGBoost weights  

Paper headline (their numbers, not ours): narrative features alone hit 93.2% macro-F1 human vs AI on long fiction. Domain is ~5k-word stories. Short chat lines are out of distribution — still score long drafts when the user cares.

## Pipeline (required)

```
draft → save file → noslop score <file> → if FAIL fix → re-score (max 2) → ship with evidence
```

1. Write under the rules below.  
2. Save non-trivial text to a file.  
3. Run from the noslop repo (or installed package):

```bash
# from C:\Users\vstal\noslop with venv active
set PYTHONPATH=src
python -m noslop.cli score path\to\draft.md
# or: python -m noslop.cli score draft.md --json
```

4. **PASS** = exit 0 (P(human) ≥ 0.5 by default). **FAIL** = exit 1.  
5. On FAIL: revise, re-score. Max 2 loops.  
6. Deliver text only with a real score result (exit code or `--json`). Never invent a pass.

Skip the gate only for tiny replies under ~80 words unless the user demands a score.

## Construction rules (write this way)

Inspired by what StoryScope measures. Not a banned-word religion.

- **Don’t preach the theme.** Let the reader get there.  
- **Leave a mess when life is messy.** One open thread, moral grey, or time jump beats a tidy moral bow.  
- **Be specific.** Names, numbers, paths, dates. Vague “landscape of…” is empty.  
- **Uneven rhythm.** Mix short and long sentences. Don’t march.  
- **Emotion:** sometimes name it. Don’t only stack body metaphors (tight chest, cold sweat, dim light).  
- **No template rhetoric.** Cut “it’s not X, it’s Y” stacks, “in today’s world,” and summary closers that restate the paragraph.  
- **Trust the reader.** Under-explain rather than over-explain.

## After FAIL

Push the draft toward human-leaning narrative choices the paper found: less explicit moralizing, less single-track causal tidiness, more concrete anchors, less sensory over-write, more genuine ambiguity where it fits the piece.

Re-run `noslop score`. Don’t synonym-cycle into more slop.

## Domain honesty

StoryScope models were trained on long fiction with 304 discourse features (default gate: `binary_narrative`, style features out). Marketing blurbs and 40-word tweets may score oddly. Say so if you score them anyway.

## Never

- Claim detector bypass or academic-fraud utility  
- Ship with “should pass” and no command output  
- Depend on Superpowers/ECC/OMC for this skill — noslop stands alone  
- Confuse this with code “deslop” tools  

## Install reminder

Repo: local `noslop` project. Artifacts + StoryScope submodule required. See project README. Runtime score path needs `numpy` + `xgboost`. Live feature extract needs an API key (`OPENAI_API_KEY`) unless you pass `--features` JSON.
