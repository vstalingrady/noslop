---
name: noslop
description: >-
  Draft or rewrite user-facing prose so it doesn’t read like template AI.
  Triggers: noslop, write human, anti AI voice, /noslop. Not for code cleanup.
  Method only — never the default topic of the draft. Draft first, then cut
  only the tells actually present; never decorate to satisfy this file.
---

# noslop

Write so a careful human finishes the page.

**This skill is a linter, not a style.** Draft from the brief first, plainly.
Then scan for tells — AI slop tells *and* noslop over-application tells — and
cut only what you actually find. If the plain draft already reads fine, ship
it unchanged. Decorating a fine draft to satisfy this file is the most common
noslop failure, and it produces a new kind of slop.

## Ship bar

```
A careful human finishes the page without fatigue or "this is a template"
nausea — and without spotting the noslop signature either.
Score-max with stiff craft = FAIL even if every scan passes.
Metrics are footnotes, never the win.
```

## Workflow

```
1. DRAFT from the brief. No checklist in hand.
2. READ like a stranger. Would a careful human finish it?
   Yes → ship. No → name the specific failure, then fix that failure only.
3. SLOP SCAN — hard bans / templates / sermon close, if present.
   [style-and-bans.md](style-and-bans.md). Zero hits = step done.
4. OVER-APPLICATION SCAN — noslop tells (below). Cut what you find.
5. LONG PROSE ONLY — if it sags structurally: fiction →
   [construction.md](construction.md) (tidy lesson, on-rails causality;
   0–3 moves, linear default); nonfiction →
   [structure-nonfiction.md](structure-nonfiction.md) (one sustained
   register; 2–4 palette picks, named skips). Linear + plain is a valid ship.
6. VOICE flags (optional) — hard fails only. There is no grade to raise.
7. SHIP when a careful human would finish the page.
```

Steps 3–6 are scans, not ingredients. A scan that finds nothing changes
nothing.

## Subject ≠ method

```
noslop = HOW you write. Never the default WHAT.
```

| User said | You do | You do **not** |
|-----------|--------|----------------|
| “use noslop” / “/noslop” / “write human” | Apply the scans **invisibly** | Write about noslop, VOICE, scores, bans, detectors, or “AI slop” |
| “analyze this repo” **and** “write a story” | Analyze in chat; story = normal fiction | Allegory of the analysis, commits, CLI, evals |
| “story **about** noslop / this project” | Topic allowed | — |

Subject check before drafting: if the piece would be about the skill, the
scores, or the repo and the user didn’t ask for that — stop, pick a real
premise.

## Slop tells (cut when present)

The full ban list lives in [style-and-bans.md](style-and-bans.md): glue words
(delve, leverage, seamless), template phrases (“In today’s…”, “It’s worth
noting”), empty openers (“Certainly,”), sermon closes, em-dash spam, rule-of-three
stacking. These are *detectors of failure*, not a list of things to avoid
thinking about — if none appear in the draft, move on.

## Noslop tells (over-application — cut when present)

Applying this skill too hard has its own signature. If the draft shows these,
**you over-applied the skill. Remove them.**

| Tell | Looks like |
|------|------------|
| **Anchor stuffing** | A number, name, time, or place crammed into every sentence; digits that don’t need to exist |
| **Fragment cosplay** | Subjectless telegraph lines with pronouns stripped, stacked for texture (“Rain. Bus plastic. Four dollars.”) |
| **Signature closer** | “If this is noise, delete it.” / “No deck.” / any performative punchy exit |
| **Punchy moral one-liner** | A single-line zinger as the last beat (“That just multiplies noise.”) |
| **Boring-detail theater** | A deliberately pointless detail inserted *to seem* human |
| **Manufactured mess** | A problem invented because a checklist said “one mess” |
| **Em-dash as personality** | Dashes used as a voice, not a punctuation choice |
| **Same skeleton** | The draft has the same shape as your last noslop draft |

Root rule: **if a rule made the text weirder, the rule was wrong for this
draft.** Delete the effect, keep the draft.

## Specifics: honest or absent

Use the real specifics the brief gives you. Invent none (no fake stats,
names, dates, anecdotes). If the brief has no specifics, write well without
them — plain and honest beats decorated. Anchors are seasoning that may be
present, never a quota to fill.

## Genre split

| Form | Rules |
|------|--------|
| **Long fiction** (stories, chapters, ~1k+) | Draft first. If structure sags, light PRE-STRUCTURE from [construction.md](construction.md): pick **0–3** moves, linear default, no tidy lesson close, diversity seed = moves you deliberately skip. Then the same two scans. |
| **Long nonfiction** (essays, reports, ~1k+) | Draft first. If it reads as one sustained register, light PRE-DRAFT from [structure-nonfiction.md](structure-nonfiction.md): pick **2–4** palette moves, seed macro choices, name the skips. Then the same two scans. |
| **Short agent prose** (email, bio, blurb, answers) | Draft + two scans. **No** novel toys (no time jumps, grey choice, aftermath construction). |
| **StoryScope features** | Lab only when asked; honest labels; never forge; never a ship gate |

## Modes

Modes = how much you interfere. Default: **balanced**.

| Mode | Interference |
|------|--------------|
| **modest** | Almost none — slop scan only. Letters, notes, anything that should feel unforced |
| **balanced** | Fix real failures, add nothing. Default |
| **max** | Research only — stress craft; expect stiffness; never ship as product voice |

See [modes.md](modes.md).

## PRE-WRITE (four lines)

For anything over ~300 words, answer before drafting (mentally is fine for
short prose):

```text
Subject:   (from the brief — never noslop/scores unless asked)
Audience:
Form / length:
Biggest risk for this piece:  (glue? sermon? over-craft? fog?)
```

That’s all. No anchor quotas, no mandatory mess, no required boring detail.

## VOICE (flags, not a grade)

Optional check before ship. Blocks on **hard fails** only:

- moral/sermon close
- ban/glue spam
- zero anchors on long prose (pure fog)

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m noslop.cli voice --text-file draft.md
```

Exit code = hard fails only. The numeric score it prints is lab diagnostics —
**do not iterate to raise it.** Iterating on the number produces exactly the
fragment-spam this skill exists to kill. Details: [voice.md](voice.md).

## StoryScope (lab)

Only when the user asks for a diagnostic. Honest labels with span cites —
never forge ([human_coding.md](human_coding.md)). Footnote only, never a ship
gate, never a writing coach. Background: [paper.md](paper.md).

## Red flags — STOP

- Rewriting a readable draft because a scan exists
- Anchor stuffing / fragment cosplay / signature closers (you over-applied)
- **Subject hijack** — draft about noslop / scores / the repo when they asked for other content
- Novel construction toys on a cold email
- Theme lecture / tidy lesson as last beat of fiction
- Iterating to raise VOICE or P(human) — that IS score-maxxing
- Shipping with hard-ban words still on the page
- Forging StoryScope feature labels

## Rationalizations

| Excuse | Reality |
|--------|---------|
| “The skill says add anchors/mess/unevenness” | Scans detect failures; they don’t order ingredients |
| “Numbers in the subject line worked last time” | One skeleton repeated = template = slop |
| “Fragments make it punchy” | Subjectless stacks are slop cosplay; keep I/you/they |
| “VOICE 9.1 so ship” | The number is a footnote; stiff craft at 9.1 is still stiff |
| “Bans are the whole skill” | Clean vocab + sermon close is still AI fiction |
| “Structure is enough; skip bans” | Surface tells still read as template AI |
| “Hit every human feature to raise P(human)” | Inverts the detector; creates a new cluster |

Refs: [style-and-bans.md](style-and-bans.md) · [construction.md](construction.md) · [structure-nonfiction.md](structure-nonfiction.md) · [modes.md](modes.md) · [voice.md](voice.md) · [checklists.md](checklists.md) · [paper.md](paper.md)
