# noslop checklists

Ship needs PRE-WRITE + VOICE PASS. StoryScope optional.

## PRE-WRITE

```text
NOSLOP PRE-WRITE
Audience:
Length / form:
Anchors (name / number / place / time):
One deliberate mess / open cost / incomplete beat:
One boring detail with no payoff:
What I will NOT force (skip: frame | twist | theme line | long aftermath):
Where short hits land:
Surface risk for this genre:
```

Rules:

- Anchors concrete, not “something specific later.”
- Mess/incomplete: skip only if form is one-line; write `N/A — too short`.
- “What I will NOT force” must name at least one skipped arc toy.

## VOICE grade

```text
NOSLOP VOICE
anchors:     0-2  PASS|FAIL
uneven:      0-2  PASS|FAIL
moral_close: 0-2  PASS|FAIL
rhythm:      0-2  PASS|FAIL
glue_bans:   0-2  PASS|FAIL
MEAN: x.x
HARD: …
MERGED: PASS|FAIL
FIX: …
```

| Axis | 2 | 0 |
|------|---|---|
| anchors | real times/names/numbers | fog |
| uneven | skip / digression / dead detail | every line pays off |
| moral_close | no sermon close | used-to-think / lesson close |
| rhythm | length varies | flat |
| glue_bans | clean | ban spam |

CLI: `python -m noslop.cli voice --text-file draft.md --json` — score ≥ 6.5, no hard_fail.

## Structure GRADE (optional extra)

```text
NOSLOP GRADE
Theme:       SCORE 0-2  PASS|FAIL|N/A
Plot:        SCORE 0-2  PASS|FAIL|N/A
Time:        SCORE 0-2  PASS|FAIL|N/A
Specificity: SCORE 0-2  PASS|FAIL|N/A
Felt life:   SCORE 0-2  PASS|FAIL|N/A
MEAN: x.x
MERGED: PASS|FAIL
FIX: …
```

Does not replace VOICE. Do not ship on GRADE alone if VOICE fails.

## StoryScope SCORE (optional diagnostic)

```text
NOSLOP SCORE (diagnostic)
coverage: x.xx
P(human): x.xx
gate: …
note: not ship gate; books mean ~0.13
```

## Surface polish

After VOICE PASS, scan [style-and-bans.md](style-and-bans.md) once.
