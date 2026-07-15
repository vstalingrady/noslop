# VOICE (primary ship gate)

Reader anti-slop axes. **Not** StoryScope. **Not** a GPTZero guarantee.

## Axes (0–2 each)

| Axis | 2 | 0 |
|------|---|---|
| anchors | names, times, places, numbers land | abstract fog only |
| uneven | incomplete beat, digression, or no-payoff detail | every paragraph “earns” |
| moral_close | no sermon / thesis close | “I used to think… turns out…” / end-of-day lesson |
| rhythm | short hits beside longer lines | flat metronome |
| glue_bans | clean of ban list + glue phrases | delve / holistic / moreover spam |

**CLI:** `python -m noslop.cli voice --text-file draft.md --json`  
**PASS:** score ≥ 6.5 and no hard_fail (moral sermon, ban spam, zero anchors on long text).

## Anti-templates (do not dump every draft)

Avoid stacking these as a checklist:

- “I’m writing this after…”
- “Here’s the turn”
- “Aftermath isn’t X. It’s Y.”
- Forced multi-scene aftermath + twist + theme-4 every piece

Those game StoryScope. Detectors and readers still smell the pattern.

## Prefer

- One deliberate **skip** (set up, don’t pay off)
- One **boring** true detail (no symbol load)
- End on image / action / cutoff — not a moral restatement
- Fragments, contractions, interrupt OK

## Genre notes

| Form | Note |
|------|------|
| Fiction | open cost OK; skip full denouement if it would sermonize |
| Email | anchors + specific ask; no “hope this finds you well” |
| Bio | one real time/place; no passion-driven fluff |
| Marketing | one concrete scene beats “unlock growth” |
| Tech answer | timestamps, commands, failed path first |
