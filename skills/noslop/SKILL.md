---
name: noslop
description: >-
  Draft or rewrite user-facing prose so it doesn’t read like template AI.
  Triggers: noslop, write human, anti AI voice, /noslop. Not for code cleanup.
  Method only — never the default topic of the draft. Prefer human flow over
  maxing VOICE or StoryScope P(human). Long fiction: structure-first sparse
  construction; ship by page judgment, not score.
---

# noslop

Write so a careful human finishes the page.

**Both pillars required — not either/or:**

| Pillar | What | Doc |
|--------|------|-----|
| **Construction** | How the story is built (theme/plot/time/agency) | [construction.md](construction.md) · [paper.md](paper.md) |
| **Style + bans** | Hard-ban words/phrases/openers, surface structure (parataxis, rule-of-three, dash budget), formatting, pre-ship check | [style-and-bans.md](style-and-bans.md) · [voice.md](voice.md) |

Long fiction: structure first (StoryScope arXiv:2604.03136) → draft → structural FIX → **mandatory ban/style pass**.  
Short agent prose: flow + anchors + **same ban list** — **no** novel toys.  
Structure without ban hygiene = still slop. Ban swaps without structure = still AI fiction.

## Subject ≠ method

```
noslop = HOW you write. Never the default WHAT.
```

| User said | You do | You do **not** |
|-----------|--------|----------------|
| “use noslop” / “/noslop” / “write human” | Apply craft **invisibly** | Write about noslop, VOICE, scores, bans, detectors, or “AI slop” |
| “analyze this repo” **and** “write a story” | Analyze in chat if needed; story = normal fiction | Allegory of the analysis, commits, CLI, evals |
| “~5k word story” with no plot | Ordinary human premise | Meta story about scoring or this tool |
| “story **about** noslop / this project” | Topic allowed | — |

If PRE-WRITE **Subject** would be the skill/scores/repo and the user didn’t ask for that → **STOP** and pick a real premise.

## Ship bar

```
A careful human finishes the page without fatigue or “this is a template” nausea.
Readable first. Do not maximize VOICE or StoryScope at the cost of flow.
Mode default = balanced. max = research only.
Score-max with stiff craft = FAIL even if numbers look great.
High P(human) or high VOICE is never “more human” by itself — page judgment is the ship bar.
Metrics are footnotes only.
```

```
NO SHIP WITHOUT:
  PRE-WRITE (Mode + Subject)
  + long fiction: PRE-STRUCTURE + diversity seed + sparse palette (2–4)
  + draft
  + structural FIX if needed (not synonym-only)
  + style-and-bans pass (hard bans gone; rhythm/punct OK)  ← REQUIRED
  + no VOICE hard_fail (sermon / ban spam / zero anchors)
  + careful reader would finish the page
Skipping the ban list because "structure is enough" = FAIL.
Skipping structure because "I banned delve" = FAIL.
Do NOT require VOICE 9+ or StoryScope P(human) ≥ 0.5.
Book-band StoryScope (~0.1–0.3) with honest labels is fine when the page flows.
```

## Genre split

| Form | Rules |
|------|--------|
| **Long fiction** (stories, chapters, ~1k+) | [construction.md](construction.md): structure before prose; sparse 2–4 moves; diversity seed; no tidy lesson close |
| **Short agent prose** (email, bio, blurb, answers) | Flow + anti-glue + real anchors — **no** novel toys (aftermath, frame/memoir, theme scales) |
| **StoryScope features** | Lab only when asked; honest labels; never forge; never sole ship gate |

## Modes

| Mode | Role |
|------|------|
| **modest** | Light skill; unforced letters/notes |
| **balanced** | **DEFAULT SHIP** — sparse construction on long fiction |
| **max** | Research / stress craft only — may over-stack; label it; expect readability cost |

See [modes.md](modes.md).

## When to use

**Use:** stories, emails, bios, reports, landing copy, long answers; user wants human-sounding prose.  
**Skip:** code cleanup; pure data dumps.

## Workflow

```
1. PRE-WRITE (Mode + Subject required; default balanced)
2. Long fiction only → PRE-STRUCTURE + diversity seed + pick 2–4 moves
   ([construction.md](construction.md)) — structure before draft
3. Draft for genre (fiction construction OR short-prose flow)
4. Structural FIX if needed (max 2 rounds) — not synonym swaps
5. STYLE PASS (required for ALL forms — short and long) — full [style-and-bans.md](style-and-bans.md):
   a. Hard-ban words / phrases / openers: zero hits
   b. Soft bans: only literal/tech sense
   c. Surface structure: length mix, no parataxis spam, no rule-of-three default, active voice
   d. Punctuation: em-dash budget (~1/500w), almost no ! spam
   e. Context formatting (email/social vs docs)
   f. Pre-ship surface check (11 silent items) + swap cheatsheet
6. VOICE hard fails only (sermon / ban spam / zero anchors on long text)
   — anti-glue floor, not a quality ladder to max
7. Optional lab: StoryScope — footnote only; never forge
8. Ship when a careful human would finish the page
   (NOT when VOICE or P(human) looks high)
```

**Order:** structure first on long fiction, then style/bans. Never reverse-only (polish a sermon). Never skip bans after good structure.

Refs: [construction.md](construction.md) · [style-and-bans.md](style-and-bans.md) · [paper.md](paper.md) · [modes.md](modes.md) · [voice.md](voice.md) · [checklists.md](checklists.md)  
Lab: [human_coding.md](human_coding.md) · [core_features.md](core_features.md)

## PRE-WRITE (required)

```text
NOSLOP PRE-WRITE
Mode: modest | balanced | max
Subject:   (what the piece is ABOUT — from the brief; not "noslop" unless asked)
Audience:
Length / form:   (short agent | long fiction)
Anchors (name / number / place / time):
One deliberate mess / open cost / incomplete beat:
One boring detail with no payoff:
What I will NOT force (short: novel toys; fiction: theme dump / tidy lesson):
Where short hits land (if natural):
Surface risk for this genre:
Subject check: no skill/score/repo meta in draft unless Subject allows — Y/N
```

Mode omitted → **balanced**.  
Subject omitted → take it from the **user’s content brief**.

### Long fiction: PRE-STRUCTURE (required)

After PRE-WRITE, fill PRE-STRUCTURE from [construction.md](construction.md) before any prose:

```text
STORY PRE-STRUCTURE
Premise / POV / Moral grain / Time shape / Tracks / Theme location
World anchors (2–4 named) / Emotion policy / Ending type
Diversity seed: one move I will NOT use
Palette picks (2–4 max): …
```

No diversity seed or stacked full palette on long fiction → **STOP**.

## Draft by genre

### Short agent prose

| Do | Don’t |
|----|--------|
| Real anchors when they help | Aftermath / twist / theme stacks |
| One concrete ask or image | Sermon or “I used to think… turns out” close |
| Digression OK if natural | Score-farm staccato |
| Clean of glue/bans (full list) | Chase VOICE 9+; skip ban scan |
| Rhythm mix, few em dashes | Template openers / “Certainly,” / “Moreover,” |

### Long fiction

| Do | Don’t |
|----|--------|
| Theme in scene / action | Narrator TED moral as ending |
| Grey choice / open cost | Single-track tidy acceptance bow |
| Time texture when length allows | Fake multi-scene aftermath on a 100-word beat |
| Specific world (names, places, mess) | Vague allusions + body-emotion formula only |
| Sparse 2–4 moves + diversity seed | Must-hit full construction pack every draft |
| Full [style-and-bans.md](style-and-bans.md) pass before ship | “Structure is enough so bans optional” |

## VOICE

Soft anti-glue. Ship blocks on **hard fails** only:

- moral/sermon close  
- ban/glue spam  
- zero anchors on long prose  

Mid-range readable prose beats a stiff 9+. Higher VOICE is **not** more human. Details: [voice.md](voice.md).

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m noslop.cli voice --text-file draft.md --json
```

## StoryScope (lab)

Only when the user asks for a diagnostic:

1. Honest labels with span cites — never forge ([human_coding.md](human_coding.md))
2. `python -m noslop.cli score --features features.json --json`
3. Footnote only — never sole ship gate
4. Do not require P(human) ≥ 0.5
5. Do not treat the binary as a writing coach

## Red flags — STOP

- No PRE-WRITE (incl. **Subject**)
- Long fiction without **PRE-STRUCTURE** / **diversity seed** / sparse palette
- Stacked full construction palette (anti-diversity cluster)
- **Subject hijack** — draft about noslop / VOICE / scores / the repo when they asked for other content
- “Use noslop” treated as license to narrate the skill
- Chasing StoryScope 0.5 or VOICE 9+ while the page is stiff (**scoremax** = fail)
- Novel toys on a cold email
- Theme lecture / tidy lesson as last beat of fiction
- FIX = synonym swaps only
- Ban/glue spam **or** shipping without a ban pass
- Forging StoryScope feature labels
- “Structure fixed it” while delve/moreover/tapestry still on the page

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “Use noslop + story → story about noslop” | Method ≠ subject |
| “Analyze repo + story → story about the repo” | Analysis stays in chat unless they asked for that topic |
| “StoryScope PASS / 0.7” | Lab metric; books ~0.13; not ship bar |
| “VOICE 9.1 so ship” | High score + stiff craft = fail |
| “Bans list is the whole skill” | Need construction **and** bans |
| “Structure is enough; skip bans” | Surface tells still read as template AI |
| “I banned words; skip structure” | Tidy theme-sermon with clean vocab is still AI fiction |
| “Force the full arc pack” | Over-complete craft smells model-made; sparse 2–4 only |
| “Email needs aftermath + twist” | Genre split — short prose doesn’t |
| “Hit every human feature to raise P(human)” | Inverts the detector; creates a new cluster |
