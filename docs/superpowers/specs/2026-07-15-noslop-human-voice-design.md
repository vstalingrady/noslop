# noslop Human-Voice Design

**Date:** 2026-07-15  
**Status:** draft for implementation  
**Repo:** `C:\Users\vstal\noslop`

## Problem

The noslop skill changes **process** (PRE-WRITE → draft → GRADE) and often improves **structure** (open threads, anchors, no moral bow). It does **not** reliably prove or force “sounds human, not AI slop.”

Evidence from A/B test (mall security guard shoe story):

| Signal | Noslop arm | Default arm |
|--------|------------|-------------|
| PRE-WRITE + GRADE | Shipped, MERGED PASS | N/A |
| Open ending / no moral close | Yes | No (tidy thrift-bin resolution + “caring first”) |
| StoryScope P(human) (19 core feats) | 0.038 FAIL | 0.091 FAIL |
| StoryScope P(human) (54 dense feats) | 0.021 FAIL | 0.031 FAIL |

Root causes:

1. **Wrong primary metric.** StoryScope XGBoost (`binary_narrative`) predicts human-vs-AI on full discourse feature vectors (265 features → 761 cols). It is not an anti-slop detector. Ablation: *more moralizing raised* P(human).
2. **Sparse fill invalidates the gate.** Host agents fill 19–54/265 features; missing → zeros → both arms AI-floor.
3. **No closed loop.** Skill grades itself on checklist axes; never revises against a measurable anti-slop / human-voice score.
4. **Two different goals conflated.** “Literary construction” ≠ “doesn’t sound like ChatGPT.” Both matter; they need separate gates.

## Success criteria (definition of done)

A system where:

1. **Agent draft loop** ships only when:
   - `NOSLOP GRADE` MERGED = PASS, **and**
   - `NOSLOP VOICE` gate = PASS (new anti-slop / human-voice scorer).
2. **A/B eval** on fixed prompts (fiction + email + bio + product blurb + agent answer): noslop arm beats default on VOICE score in ≥4/5 prompts, and never ships a moral-close sermon on fiction.
3. **StoryScope score is secondary** (optional, coverage-gated). Never sole ship gate unless `features_extracted / features_expected ≥ 0.8`.
4. Skill text + CLI + eval harness are consistent; one command reproduces the gate.

Non-goals (v1):

- Retrain a new human/AI XGBoost on custom data (v2 candidate).
- Perfect literary quality for all genres.
- Code “deslop.”

## Approaches considered

### A — Double down on StoryScope only

Full LLM extract of 265 features → score → skill optimizes high-gain features.

- Pros: reuses existing model; paper-aligned.
- Cons: model misaligned with anti-slop; expensive extract; ablation shows moralizing can help P(human).

### B — Dual gate: structure GRADE + voice scorer (recommended)

Keep PRE-WRITE/GRADE. Add deterministic + rubric **VOICE** score that measures what “slop” means operationally. StoryScope optional with coverage warning.

- Pros: optimizes the right thing; cheap; agent-loop friendly; testable without LLM.
- Cons: heuristics can be gamed; need careful design + human spot-check.

### C — Train custom slop classifier

Labeled human vs LLM-slop corpus → new model.

- Pros: best long-term metric.
- Cons: data + train cost; not v1.

**Recommendation: B now, C later.** Keep StoryScope as optional secondary probe (A lite).

## Design (Approach B)

### Components

```
skills/noslop/          agent skill (PRE-WRITE, GRADE, VOICE, ship rules)
src/noslop/
  voice.py              VOICE feature extract + score (deterministic)
  grade_parse.py        parse GRADE blocks from agent text (optional)
  score.py              existing StoryScope score (coverage warning)
  eval_run.py           A/B eval harness
  cli.py                score-voice | score | eval
evals/
  prompts.json          fixed briefs
  gold_notes.md         what PASS/FAIL should look like
  fixtures/             sample drafts with expected gates
docs/superpowers/plans/ implementation plan
```

### Dual ship gate

```
SHIP iff:
  GRADE.MERGED == PASS
  AND VOICE.gate == PASS
  AND (optional) if --storyscope: coverage >= 0.8 AND p_human >= threshold
```

### VOICE scorer (v1) — what “human not slop” means in numbers

Deterministic signals from draft text (no LLM required for gate):

| Feature | Direction human/good | How measured |
|---------|----------------------|--------------|
| `ban_hits` | lower | count / rate of style-and-bans tokens |
| `moral_close` | 0 | last 1–2 paras match sermon patterns (“lesson”, “realized that”, “caring first”, “still checked…”) |
| `tidy_bow` | 0 for fiction | epilogue that resolves all mystery with coincidence (heuristics + genre flag) |
| `anchor_density` | higher | proper nouns + digits + clock/date patterns per 100 words |
| `rhythm_var` | higher | stdev of sentence length (tokens); penalize near-uniform |
| `em_dash_rate` | moderate | too many em-dashes → slop-ish |
| `listicle_glue` | lower | “Moreover/Furthermore/In conclusion/It’s important to note” |
| `abstract_fog` | lower | ratio of abstract nouns without concrete modifiers in openers |
| `second_person_generic` | lower for most genres | “you might be wondering” filler |
| `open_thread` | 1 for fiction when intended | optional: detect unresolved question markers if PRE-WRITE claims one |

**Score:** weighted 0–1 `voice_score`; PASS if `voice_score >= 0.55` (tunable) and hard fails none of: `moral_close`, critical ban spam, zero anchors on long text.

**Hard FAIL (always):**

- Fiction/long prose with detected moral-close sermon
- Zero anchors on pieces ≥150 words
- Ban-hit rate above absolute ceiling

### Agent loop (skill)

```
1. PRE-WRITE (unchanged shape)
2. Draft
3. GRADE (structure)
4. VOICE (run CLI or fill VOICE checklist from same axes)
5. If either FAIL → structural FIX targeting failed axes only (max 2 rounds)
6. Ship with GRADE + VOICE evidence
```

VOICE checklist (agent-visible, parallel to GRADE):

```text
NOSLOP VOICE
ban_hits:     N  PASS|FAIL
moral_close:  0|1  PASS|FAIL
anchors:      N per 100w  PASS|FAIL
rhythm_var:   x.x  PASS|FAIL
glue_phrases: N  PASS|FAIL
MEAN proxy / CLI voice_score: x.xx
MERGED: PASS|FAIL
FIX: …
```

CLI is source of truth when available; agent fill is fallback offline.

### StoryScope role (demoted)

- `score --features` keeps working.
- Add `coverage = extracted/expected`; if coverage < 0.8, report `warning: sparse_features; do_not_use_as_ship_gate` and never return gate pass for ship purposes (or gate becomes `inconclusive`).
- Optional later: `extract` subcommand for full 265 via LLM — not required for v1 ship.

### Eval harness

Fixed prompts (min 5):

1. Fiction (shoe/mall — already have)
2. Cold email
3. Personal bio
4. SaaS landing paragraph
5. Long agent technical answer

Protocol:

1. Generate default draft (no skill)
2. Generate noslop draft (full skill)
3. Score both with VOICE + GRADE parse
4. Pass if noslop VOICE > default VOICE and noslop hard-fails == 0

Regression fixtures: store known good/bad drafts under `evals/fixtures/`.

### Skill install path

Single source: `C:\Users\vstal\noslop\skills\noslop\`  
Mirror to `%USERPROFILE%\.claude\skills\noslop\` and `.grok`/agents skill dirs as needed after changes.

## Risks

| Risk | Mitigation |
|------|------------|
| Heuristics gamed by synonym soup | Hard fail on moral_close + anchors; structure GRADE still required |
| Fiction-only heuristics hurt email | Genre flag from PRE-WRITE Length/form |
| Overfit to ban list | Weight bans low; rhythm + anchors + moral_close dominate |
| Agents skip CLI | Skill requires VOICE block; eval CI runs CLI |

## Open decisions (locked for v1)

1. Primary ship metric = **VOICE + GRADE**, not StoryScope.
2. StoryScope coverage gate = 0.8 for any use as secondary signal.
3. Max rewrite rounds = 2 (unchanged).
4. No new ML train in v1.

## Approval

Implement per `docs/superpowers/plans/2026-07-15-noslop-human-voice.md`.
