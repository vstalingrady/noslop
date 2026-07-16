# noslop checklists

Ship: PRE-WRITE + (long fiction: PRE-STRUCTURE) + no VOICE hard_fail + **readable page**.  
StoryScope optional (lab). Structure: [construction.md](construction.md) · [paper.md](paper.md).

## PRE-WRITE

```text
NOSLOP PRE-WRITE
Mode: modest | balanced | max
Subject:   (piece topic/plot — not noslop/scores/skill unless user asked)
Audience:
Length / form:   (short agent | long fiction)
Anchors (name / number / place / time):
One deliberate mess / open cost / incomplete beat:
One boring detail with no payoff:
What I will NOT force:
Where short hits land (if natural):
Surface risk for this genre:
Subject check: no skill/score/repo meta in draft unless Subject allows — Y/N
```

Rules:

- Mode default = **balanced** if omitted. **max** = research only.
- **Subject ≠ method:** noslop is HOW. If Subject is the tool/scores/repo and user didn’t ask for that topic → FAIL PRE-WRITE; take a real premise.
- Anchors concrete, not “something specific later.”
- Mess/incomplete: skip only if form is one-line; write `N/A — too short`.
- **Short agent prose:** “What I will NOT force” includes at least one **novel toy** (frame / twist / multi-scene aftermath / theme scale).
- **Long fiction:** include **theme dump** and/or **tidy single-track lesson close** in “What I will NOT force.”
- See [modes.md](modes.md) · [SKILL.md](SKILL.md) · [construction.md](construction.md).

## PRE-STRUCTURE (long fiction only)

Required **before prose**. Full guide: [construction.md](construction.md).

```text
NOSLOP PRE-STRUCTURE
Premise:
POV:
Moral grain:          (grey choice / open cost)
Time shape:           linear | one jump | frame | braided
Tracks:               spine + optional B / loose end
Theme location:       scene/action only
World anchors:        2–4 named
Emotion policy:       mix named + body; no body-every-paragraph
Ending type:          (acceptance-bow banned unless earned)
Diversity seed:       one human-leaning move I will NOT use
Palette picks (2–4):  …
Anti-AI refused:      theme dump | single-track tidy | setting-as-mood spam
```

- No diversity seed → FAIL for long fiction.
- Stacking all palette moves → FAIL (new cluster).
- Skip this entire block for emails/bios/blurbs.

## VOICE grade

```text
NOSLOP VOICE
anchors:     0-2  PASS|FAIL
uneven:      0-2  PASS|FAIL
moral_close: 0-2  PASS|FAIL
rhythm:      0-2  PASS|FAIL
glue_bans:   0-2  PASS|FAIL
MEAN: x.x   (informative — do not max; higher ≠ more human)
HARD: none | moral_close_sermon | ban_spam | zero_anchors
MERGED: PASS|FAIL   (FAIL only on HARD)
FIX: …
```

| Axis | 2 | 0 |
|------|---|---|
| anchors | real times/names/numbers | fog |
| uneven | skip / digression / dead detail | every line pays off |
| moral_close | no sermon close | used-to-think / lesson close |
| rhythm | length varies naturally | flat or forced staccato show |
| glue_bans | clean | ban spam |

CLI: `python -m noslop.cli voice --text-file draft.md --json`  
**Ship block:** `hard_fail` only (anti-glue floor). Page judgment is still required.

## Fiction construction (long form only)

After draft, confirm structure — not score farming:

```text
NOSLOP FICTION (long form)
PRE-STRUCTURE filled?              Y/N
Diversity seed set?                Y/N
Palette sparse (2–4 only)?         Y/N
Theme dump avoided?                Y/N
Grey choice / open cost?           Y/N
Time texture if length allows?     Y/N/N/A
Tidy single-track lesson close avoided? Y/N
Structural FIX used if needed (not synonym-only)? Y/N/N/A
Page would finish for a careful reader? Y/N
```

Skip for emails/bios/blurbs. See [construction.md](construction.md).

## StoryScope SCORE (lab)

```text
NOSLOP SCORE (lab)
coverage: x.xx
P(human): x.xx
note: footnote only; books mean ~0.13; never forge; never ship gate
```

## Surface polish + bans (required — all forms)

Not optional. Not “once if you feel like it.” Run after structure/draft; before ship.

```text
NOSLOP STYLE+BANS
Hard-ban words:     0 hits?     Y/N
Hard-ban phrases:   0 hits?     Y/N
Hard-ban openers:   0 hits?     Y/N   (Certainly, Moreover, Great question!, …)
Template patterns:  0 hits?     Y/N   (Not just X but Y, In a world where, …)
Parataxis spam:     gone?       Y/N   (not Short. Short. Short. whole para)
Rule of three:      broken?     Y/N
Em dashes:          ~≤1/500w?   Y/N
Rhythm:             mixed?      Y/N
Active / no pep:    OK?         Y/N
Format context:     OK?         Y/N   (no md headers in email, etc.)
Honesty:            no invents? Y/N
Pre-ship 11-check:  done?       Y/N
Soft bans:          only literal/tech? Y/N
```

Full lists + swaps + 11-check: [style-and-bans.md](style-and-bans.md).  
Polish last on long fiction — never a substitute for PRE-STRUCTURE.  
Never a substitute to skip this after good structure.
