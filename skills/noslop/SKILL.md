---
name: noslop
description: >-
  Use when drafting or rewriting user-facing prose that must not read as AI-slop,
  or when the user says noslop, write human, anti AI voice, or /noslop. Not for
  code cleanup. North star: StoryScope construction findings + human flow — not
  maxing VOICE or StoryScope P(human).
---

# noslop

Grounded in StoryScope (arXiv:2604.03136): AI prose often **over-explains themes** and runs **tidy single-track** arcs; humans leave **greyer choices**, **messier time**, and more **diversity**. Full paper notes: [paper.md](paper.md).

## Ship bar (iron law)

```
Ship bar: careful human finishes the page without fatigue or template nausea.
Do not maximize VOICE or StoryScope at the cost of flow.
Mode default = balanced. max = research only.
Score-max with stiff craft = FAIL even if numbers look great.
```

**Violating the letter of these rules is violating the spirit of the rules.**

```
NO SHIP WITHOUT: PRE-WRITE (incl. Mode) + draft + no VOICE hard_fail
Do NOT require VOICE 9+ or StoryScope P(human) ≥ 0.5.
Book-band StoryScope (~0.1–0.3) with honest labels is OK when the page flows.
```

## Genre split (critical)

| Form | Primary rules |
|------|----------------|
| **Long fiction** (stories, chapters, ~1k+ words) | Paper construction: less theme lecture, greyer moral choice, temporal texture when length allows, avoid tidy single-track lesson close + flow |
| **Short agent prose** (email, bio, blurb, answers) | Flow + anti-glue + anchors when natural — **do not** force novel discourse toys (extended aftermath, frame/memoir, theme scales, multi-scene moral arc) |
| **StoryScope score / features** | Lab only; long-form or explicit research; honest extract/label; never forge; never ship gate |

## Modes

See [modes.md](modes.md).

| Mode | Role |
|------|------|
| **modest** | Unforced letters/notes; light skill |
| **balanced** | **DEFAULT SHIP** |
| **max** | Research / stress craft only — label it; expect readability cost |

## When to use / not

**Use:** stories, emails, bios, reports, landing copy, long agent answers; user wants human-sounding / less slop / noslop.  
**Skip:** code cleanup; pure data dumps where voice does not matter.

## Core pattern

```
1. Fill NOSLOP PRE-WRITE (Mode required; default balanced)
2. Draft for the genre (fiction construction OR short-prose flow — see split)
3. Check VOICE for hard fails only (sermon close, ban/glue spam, zero anchors on long text)
4. FAIL hard → structural FIX (max 2 rounds) — not synonym swaps
5. Surface ban scan once ([style-and-bans.md](style-and-bans.md))
6. Optional lab: StoryScope features + score — footnote only
7. Ship when a careful human would finish the page
```

Refs: [paper.md](paper.md) · [modes.md](modes.md) · [voice.md](voice.md) · [checklists.md](checklists.md) · [style-and-bans.md](style-and-bans.md)  
Lab only: [human_coding.md](human_coding.md) · [core_features.md](core_features.md)

## PRE-WRITE (required)

```text
NOSLOP PRE-WRITE
Mode: modest | balanced | max
Audience:
Length / form:   (short agent | long fiction)
Anchors (name / number / place / time):
One deliberate mess / open cost / incomplete beat:
One boring detail with no payoff:
What I will NOT force (for short: skip novel toys; for fiction: skip theme dump / tidy lesson):
Where short hits land (if natural):
Surface risk for this genre:
```

If Mode omitted → **balanced**.

## Draft by genre

### Short agent prose (default for emails, bios, blurbs, Q&A)

| Do | Don’t |
|----|--------|
| Real anchors when they help | Force aftermath / twist / theme-4 stacks |
| One concrete ask or image | Sermon or “I used to think… turns out” close |
| Digression OK if natural | Score-farm staccato every line “earns” |
| Clean of glue/bans | Chase VOICE 9+ |

### Long fiction (paper construction)

| Do | Don’t |
|----|--------|
| Theme in scene / action, not narrator TED talk | Explicit moral restatement as ending |
| Grey choice / open cost | Single-track tidy internal-acceptance bow |
| Time texture when length allows (jump, delay, flash) | Fake multi-scene aftermath on a 100-word beat |
| Specific world (names, places, real mess) | Vague allusions + body-emotion formula only |

**modest:** lighter still. **max:** full craft pressure (research); label it.

## VOICE (soft anti-glue — not human-quality score)

Hard fails only for ship block:

- moral/sermon close
- ban/glue spam
- zero anchors on long prose

Prefer mid-range readable prose over a 9+ checklist. Details: [voice.md](voice.md).

```powershell
cd path\to\noslop
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m noslop.cli voice --text-file draft.md --json
```

## StoryScope (lab only)

Only if user asks for diagnostic:

1. Honest labels with span cites — never forge ([human_coding.md](human_coding.md))
2. `python -m noslop.cli score --features features.json --json`
3. Footnote only — **never** sole ship gate
4. Do not require P(human) ≥ 0.5

## Red flags — STOP

- Shipping without PRE-WRITE
- Chasing StoryScope 0.5 or VOICE 9+ while the page is stiff
- Novel toys on a cold email
- Theme lecture / tidy lesson as last beat of fiction
- FIX = synonym swaps only
- Thesis closer as last paragraph
- Ban/glue spam

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “StoryScope says PASS / 0.7” | Lab metric; books ~0.13; not ship bar |
| “VOICE is 9.1 so ship” | High score + stiff craft = fail |
| “Bans list is the skill” | Construction + flow first; paper.md |
| “I’ll force the full arc pack” | Anti-template; over-complete craft smells model-made |
| “Email needs aftermath + twist” | Genre split — short prose doesn’t |
