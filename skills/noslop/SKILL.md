---
name: noslop
description: >-
  Use when drafting or rewriting prose that should read human (articles, emails,
  stories, bios, reports, tweets, long answers), or when the user says noslop,
  write human, anti AI voice, or /noslop. Structure-first; not code cleanup.
---

# noslop

Human writing is **built** differently, not just word-swapped. Gate with five parallel structure checks. No required local model. No mandatory CLI.

## Pipeline

```
1. WRITE under structure rules
2. FAN-OUT 5 grader subagents (same draft, different axes)
3. MERGE verdicts → PASS or FAIL
4. If FAIL: fix only what failed → one re-grade (max 2 rounds)
5. Ship draft. Do not invent a pass.
```

Short text is fine (tweets too). Graders still run; they just have less evidence.

## Write rules (structure)

Do these while drafting. Not a banned-word religion.

- Don’t preach the theme. No closing sermon.
- Don’t over-tidy. Leave a loose end, grey choice, or jump when it fits.
- Specifics: names, numbers, times, concrete nouns. Not fog.
- Uneven rhythm. Mix short and long.
- Emotion: name it sometimes. Don’t only stack body metaphors.
- No template rhetoric stacks (“it’s not X, it’s Y” spam, restatement closers).
- Trust the reader. Under-explain.

## Fan-out: 5 graders

Spawn **5 independent graders in parallel** (subagents or separate calls).  
Each gets: full draft + **only its axis**.  
Each returns **only** the block below. No rewrites in the grader pass.

| # | Axis | Fail if |
|---|------|---------|
| 1 | **Theme** | Narrator/author states the moral/lesson; over-explains meaning |
| 2 | **Plot / argument** | Everything resolves too cleanly; single-track with no friction; every para restates itself |
| 3 | **Time / order** | Only rigid march with no jump, aside, or delayed reveal when the piece is long enough to allow one |
| 4 | **Specificity** | Vague grandeur; no names/numbers/places/paths; only generic claims |
| 5 | **Felt life** | Emotion only via body/sense catalog; zero plain feeling words; or zero human mess/doubt |

For very short text (&lt;~50 words): axes 2–3 may return `N/A` (not enough room). Count only scored axes.

### Grader system prompt (paste per agent)

```text
You are grader axis: {AXIS_NAME}.
Judge STRUCTURE only. Ignore banned-word vibes unless they change meaning.

Draft:
---
{DRAFT}
---

Return exactly:
AXIS: {AXIS_NAME}
SCORE: 0-2   (0=AI-shaped, 1=mixed, 2=human-shaped)
VERDICT: PASS | FAIL | N/A
WHY: one sentence, concrete, cite a span if possible
FIX: one structural change if FAIL, else none
```

Axis names: `Theme` | `Plot` | `Time` | `Specificity` | `Felt life`

### Merge rule

- Drop `N/A`.
- **PASS** if mean SCORE ≥ 1.2 and no more than one FAIL.
- **FAIL** otherwise.
- On FAIL: apply the FIX lines (structure only), rewrite draft, re-run all 5 once more. Stop after 2 full grade rounds.

## How to fan out

Prefer parallel subagents (one axis each). Same draft text to all. No shared chain-of-thought between graders.

If subagents unavailable: five sequential calls with the same grader template still OK — worse latency, same logic.

## Optional local scorer

Repo `noslop` CLI + XGBoost exists if you want offline numbers later. **Not required.** This skill is prompt + 5 graders.

## Never

- Ship on vibes without the 5-way merge (unless user said skip gate).
- Fix “style” only (synonym swaps) when FAIL was structural.
- Claim detector bypass.
- Confuse with code deslop tools.
