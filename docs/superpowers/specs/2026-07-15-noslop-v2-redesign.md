# noslop v2 Redesign

**Date:** 2026-07-15  
**Status:** design for implementation  
**Repo:** `C:\Users\vstal\noslop`

## Why redesign (evidence)

| Test | Result |
|------|--------|
| StoryScope A/B (v1 skill) | noslop >> default (Δ ≥ 0.5) — **metric win** |
| Human books on StoryScope | mean P(human) **0.13** vs noslop **0.58** — books look “more AI” |
| Forced must-hit on book maps | jumps to ~0.56–0.70 — **feature gaming** |
| GPTZero on noslop sample | **Highly confident AI generated** — **detector fail** |

**Root cause:** v1 optimized a single scoreboard (StoryScope human-class construction pack). That pack fights:

1. Literary human prose (Hemingway-like: low theme, no neat aftermath stack)
2. Commercial detectors (GPTZero: surface stats, even “craft”)
3. Reader “slop” sense (perfect arc + thesis close still smells model)

## Product goal (v2)

**Primary:** Prose that reads as human to a careful reader and fails fewer *obvious* AI tells — **not** max StoryScope P(human).

**Secondary:** Optional StoryScope probe (diagnostic only; never sole ship gate).

**Non-goals:** Guaranteed GPTZero pass; adversarial detector evasion as a product claim; retrain StoryScope XGBoost in v1 of this redesign.

## Success criteria (definition of done)

1. **Reader / anti-slop gate (primary)**  
   On ≥5 fixed briefs, noslop draft beats default on a **Voice/Slop rubric** (0–10, mean ≥6.5 and ≥ default+1.5) scored from prose rules (see VOICE), with hard FAIL on moral-close sermon + ban-spam + zero anchors.

2. **Detector sanity (secondary, best-effort)**  
   Where GPTZero (or similar) is runnable: noslop arm must not be *worse* than default on “AI probability” more often than 1/5 briefs; target **AI% ≤ default AI%** on ≥3/5. Document tool + model version. No claim of “undetectable.”

3. **StoryScope demoted**  
   CLI may still score; ship does **not** require P(human) ≥ 0.5. If StoryScope used, log only; warn if coverage &lt; 0.3 or if must-hit stack is the only reason for high score.

4. **Human baseline honesty**  
   Eval includes book excerpts; skill docs state StoryScope books baseline and that high P(human) ≠ literary.

5. **Skill install**  
   Updated `skills/noslop/*` mirrored to `%USERPROFILE%\.claude\skills\noslop\`.

6. **Sample**  
   At least one shipped sample that: (a) passes VOICE gate vs a default rewrite of same brief, (b) is re-checked in GPTZero if available — result recorded even if still “AI.”

## Architecture: triple layer, one primary gate

```
brief
  → PRE-WRITE (v2: mess, skip, noise — not only aftermath/twist)
  → DRAFT (voice-first construction)
  → VOICE grade (primary ship)
  → SURFACE scan (bans + glue + moral close)
  → optional: detector probe
  → optional: StoryScope features (diagnostic)
  → FIX max 2 rounds targeting failed primary axes
  → ship with VOICE evidence
```

### Layer A — VOICE (primary)

Deterministic + checklist axes (agent or CLI `noslop voice`):

| Axis | Good | Bad |
|------|------|-----|
| Anchors | names, times, places, numbers | abstract fog |
| Unevenness | one incomplete beat, digression, or wasted detail | every paragraph “earns” |
| Moral close | absent / implied only | “I used to think… turns out…” closer |
| Rhythm | sentence length variance high | metronome short-long-short |
| Glue / bans | low | delve, tapestry, holistic, moreover… |
| Over-complete arc | optional frame/twist; may skip | checklist dump: frame+twist+theme+aftermath all forced |
| Specific mess | grey choice or open cost | tidy bow for every genre |

**VOICE score 0–10:** weighted sum. **PASS ≥ 6.5** and no hard FAIL.

### Layer B — Surface (always)

`style-and-bans.md` after VOICE pass (or final pass). Does not replace VOICE.

### Layer C — StoryScope (optional diagnostic)

- Fill features only if user asks for StoryScope.
- Default skill path: **do not** force extended aftermath + theme 4 + twist + frame every time.
- Doc: books mean ~0.13; do not chase 0.5 as literary truth.

### Layer D — Detector probe (optional)

- Script or manual: paste into GPTZero / local proxy.
- Record AI%; compare arms.
- Never ship-gate alone (brittle API, ToS, model drift).

## Skill recipe changes (v2)

### Drop as hard requirements

- Extended aftermath every piece  
- Climactic end twist every piece  
- Theme surface 3–4 every piece  
- Frame/memoir every piece  
- Ship requires StoryScope P(human) ≥ 0.5  

### Keep (softer, genre-aware)

- Anchors when length allows  
- Embodied or behavioral feeling (not only labels)  
- At least one deliberate mess / open thread / cost  
- Vary rhythm  
- Ban list after structure  

### Add (anti-GPTZero / anti-even-craft)

- **One intentional skip:** something set up that does not pay off  
- **One boring true detail:** no symbolic load  
- **Asymmetric paragraphs:** one very short; one rambling  
- **No thesis close:** end on image, action, or cutoff — not moral restatement  
- **Local voice:** contraction, fragment, interrupt allowed  
- **Anti-pattern list:** “I’m writing this after…”, “Here’s the turn”, “Aftermath isn’t X” as *templates* (allowed only if organic, not every draft)

### PRE-WRITE v2

```text
NOSLOP PRE-WRITE
Audience:
Length / form:
Anchors (name / number / place / time):
One deliberate mess / open cost / incomplete beat:
One boring detail with no payoff:
What I will NOT do (skip arc piece: frame | twist | theme line | long aftermath):
Where short hits land:
Surface risk for this genre:
```

### GRADE v2 (VOICE)

```text
NOSLOP VOICE
anchors:     0-2  PASS|FAIL
uneven:      0-2  PASS|FAIL
moral_close: 0-2  PASS|FAIL  (2 = clean no sermon)
rhythm:      0-2  PASS|FAIL
glue_bans:   0-2  PASS|FAIL
MEAN: x.x
HARD: (any hard fail?)
MERGED: PASS|FAIL
FIX: …
```

## Eval harness v2

| Brief set | same 5 + optional new |
|-----------|------------------------|
| Arms | default, noslop-v2 |
| Metrics | VOICE score, ban hits, moral_close flag, optional GPTZero AI%, optional StoryScope P(human) as footnote |
| Human refs | keep `evals/results/human/` as calibration, not ship gate |
| Pass | VOICE criteria (success #1); detector sanity if tool present (#2) |

## Risks

| Risk | Mitigation |
|------|------------|
| “Mess” becomes random garbage | Anchors + length still required |
| Detectors still flag all LLM text | Document best-effort; no guarantee |
| Users still want StoryScope 0.5 | Optional “legacy storyscope mode” skill flag |
| Agents ignore VOICE | Iron law: no ship without VOICE block |

## Approaches considered

| Approach | Verdict |
|----------|---------|
| A — Only StoryScope harder | Rejected — proven misaligned with books + GPTZero |
| B — Only ban lists | Rejected — surface without construction |
| C — **Voice-first dual eval + demote StoryScope** | **Chosen** |
| D — Train new detector | Later / out of scope for skill redesign |

## Approval

Implement per `docs/superpowers/plans/2026-07-15-noslop-v2.md`.
