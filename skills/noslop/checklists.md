# noslop checklists

Ship: PRE-WRITE + no VOICE hard_fail + **readable page**.  
StoryScope optional (lab). See [paper.md](paper.md).

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
- **Long fiction:** include **theme dump** and/or **tidy single-track lesson close**.
- See [modes.md](modes.md) · [SKILL.md](SKILL.md).

## VOICE grade

```text
NOSLOP VOICE
anchors:     0-2  PASS|FAIL
uneven:      0-2  PASS|FAIL
moral_close: 0-2  PASS|FAIL
rhythm:      0-2  PASS|FAIL
glue_bans:   0-2  PASS|FAIL
MEAN: x.x   (informative — do not max)
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
**Ship block:** `hard_fail` only.

## Fiction construction (long form only)

```text
NOSLOP FICTION (long form)
Theme dump avoided?     Y/N
Grey choice / open cost? Y/N
Time texture if length allows? Y/N/N/A
Tidy single-track lesson close avoided? Y/N
```

Skip for emails/bios/blurbs.

## StoryScope SCORE (lab)

```text
NOSLOP SCORE (lab)
coverage: x.xx
P(human): x.xx
note: footnote only; books mean ~0.13; never forge
```

## Surface polish

After no hard_fail, scan [style-and-bans.md](style-and-bans.md) once.
