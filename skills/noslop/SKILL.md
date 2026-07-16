---
name: noslop
description: >-
  Draft or rewrite user-facing prose so it doesn’t read like template AI.
  Triggers: noslop, write human, anti AI voice, /noslop. Not for code cleanup.
  Method only — never the default topic of the draft. Prefer human flow over
  maxing VOICE or StoryScope P(human).
---

# noslop

Write so a careful human finishes the page.

Long fiction follows StoryScope construction (arXiv:2604.03136): greyer choices, messier time when length allows, less theme lecture. Short agent prose uses flow, anchors, and anti-glue. Details: [paper.md](paper.md).

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
```

```
NO SHIP WITHOUT: PRE-WRITE (Mode + Subject) + draft + no VOICE hard_fail
Do NOT require VOICE 9+ or StoryScope P(human) ≥ 0.5.
Book-band StoryScope (~0.1–0.3) with honest labels is fine when the page flows.
```

## Genre split

| Form | Rules |
|------|--------|
| **Long fiction** (stories, chapters, ~1k+) | Less theme dump; greyer choice; time texture when length allows; no tidy lesson close |
| **Short agent prose** (email, bio, blurb, answers) | Flow + anti-glue + real anchors — **no** novel toys (aftermath, frame/memoir, theme scales) |
| **StoryScope features** | Lab only when asked; honest labels; never forge; never sole ship gate |

## Modes

| Mode | Role |
|------|------|
| **modest** | Light skill; unforced letters/notes |
| **balanced** | **DEFAULT SHIP** |
| **max** | Research / stress craft only — label it; expect readability cost |

See [modes.md](modes.md).

## When to use

**Use:** stories, emails, bios, reports, landing copy, long answers; user wants human-sounding prose.  
**Skip:** code cleanup; pure data dumps.

## Workflow

```
1. PRE-WRITE (Mode + Subject required; default balanced)
2. Draft for genre (fiction construction OR short-prose flow)
3. VOICE hard fails only (sermon / ban spam / zero anchors on long text)
4. FAIL → structural FIX (max 2 rounds) — not synonym swaps
5. Ban scan once ([style-and-bans.md](style-and-bans.md))
6. Optional lab: StoryScope — footnote only
7. Ship when a careful human would finish the page
```

Refs: [paper.md](paper.md) · [modes.md](modes.md) · [voice.md](voice.md) · [checklists.md](checklists.md) · [style-and-bans.md](style-and-bans.md)  
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

## Draft by genre

### Short agent prose

| Do | Don’t |
|----|--------|
| Real anchors when they help | Aftermath / twist / theme stacks |
| One concrete ask or image | Sermon or “I used to think… turns out” close |
| Digression OK if natural | Score-farm staccato |
| Clean of glue/bans | Chase VOICE 9+ |

### Long fiction

| Do | Don’t |
|----|--------|
| Theme in scene / action | Narrator TED moral as ending |
| Grey choice / open cost | Single-track tidy acceptance bow |
| Time texture when length allows | Fake multi-scene aftermath on a 100-word beat |
| Specific world (names, places, mess) | Vague allusions + body-emotion formula only |

## VOICE

Soft anti-glue. Ship blocks on **hard fails** only:

- moral/sermon close  
- ban/glue spam  
- zero anchors on long prose  

Mid-range readable prose beats a stiff 9+. Details: [voice.md](voice.md).

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

## Red flags — STOP

- No PRE-WRITE (incl. **Subject**)
- **Subject hijack** — draft about noslop / VOICE / scores / the repo when they asked for other content
- “Use noslop” treated as license to narrate the skill
- Chasing StoryScope 0.5 or VOICE 9+ while the page is stiff
- Novel toys on a cold email
- Theme lecture / tidy lesson as last beat of fiction
- FIX = synonym swaps only
- Ban/glue spam

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “Use noslop + story → story about noslop” | Method ≠ subject |
| “Analyze repo + story → story about the repo” | Analysis stays in chat unless they asked for that topic |
| “StoryScope PASS / 0.7” | Lab metric; books ~0.13; not ship bar |
| “VOICE 9.1 so ship” | High score + stiff craft = fail |
| “Bans list is the whole skill” | Construction + flow first |
| “Force the full arc pack” | Over-complete craft smells model-made |
| “Email needs aftermath + twist” | Genre split — short prose doesn’t |
