# noslop checklists

Ship needs PRE-WRITE + no VOICE hard_fail + **human-readable page**.  
StoryScope optional (lab). See [paper.md](paper.md).

## PRE-WRITE

```text
NOSLOP PRE-WRITE
Mode: modest | balanced | max
Audience:
Length / form:   (short agent | long fiction)
Anchors (name / number / place / time):
One deliberate mess / open cost / incomplete beat:
One boring detail with no payoff:
What I will NOT force:
Where short hits land (if natural):
Surface risk for this genre:
```

Rules:

- Mode default = **balanced** if omitted. **max** = research only.
- Anchors concrete, not “something specific later.”
- Mess/incomplete: skip only if form is one-line; write `N/A — too short`.
- **Short agent prose:** “What I will NOT force” must include at least one **novel toy** (frame / twist / multi-scene aftermath / theme scale).
- **Long fiction:** “What I will NOT force” should include **theme dump** and/or **tidy single-track lesson close** (paper).
- See [modes.md](modes.md).

## VOICE grade (soft)

```text
NOSLOP VOICE
anchors:     0-2  PASS|FAIL
uneven:      0-2  PASS|FAIL
moral_close: 0-2  PASS|FAIL
rhythm:      0-2  PASS|FAIL
glue_bans:   0-2  PASS|FAIL
MEAN: x.x   (informative only — do not max)
HARD: none | moral_close_sermon | ban_spam | zero_anchors
MERGED: PASS|FAIL   (FAIL only on HARD)
FIX: …
```

| Axis | 2 | 0 |
|------|---|---|
| anchors | real times/names/numbers | fog |
| uneven | skip / digression / dead detail | every line pays off |
| moral_close | no sermon close | used-to-think / lesson close |
| rhythm | length varies naturally | flat **or** forced staccato show |
| glue_bans | clean | ban spam |

CLI: `python -m noslop.cli voice --text-file draft.md --json`  
**Ship block:** `hard_fail` only. Do **not** require mean ≥ 6.5 or 9 as “human quality.”

## Fiction construction (long form only)

```text
NOSLOP FICTION (long form)
Theme dump avoided?     Y/N
Grey choice / open cost? Y/N
Time texture if length allows? Y/N/N/A
Tidy single-track lesson close avoided? Y/N
```

Does not apply to emails/bios/blurbs. Does not replace readability.

## StoryScope SCORE (lab footnote only)

```text
NOSLOP SCORE (lab)
coverage: x.xx
P(human): x.xx
note: not ship gate; books mean ~0.13; never forge
```

## Surface polish

After no hard_fail, scan [style-and-bans.md](style-and-bans.md) once.
