# VOICE

Soft anti-glue check on the draft. Complements StoryScope (lab); not a “human quality” ladder to maximize.

Ship on **hard fails** and whether a careful person finishes the page.  
Mid VOICE with natural flow beats a stiff 9+.

Paper: [paper.md](paper.md).

## Axes (0–2 each)

| Axis | 2 | 0 |
|------|---|---|
| anchors | names, times, places, numbers | abstract fog only |
| uneven | incomplete beat, digression, or no-payoff detail | every paragraph “earns” |
| moral_close | no sermon / thesis close | “I used to think… turns out…” / end-of-day lesson |
| rhythm | short hits beside longer lines | flat metronome or forced staccato skill-show |
| glue_bans | clean of ban list + glue phrases | delve / holistic / moreover spam |

**CLI:** `python -m noslop.cli voice --text-file draft.md --json`

## Ship use

| Block ship | Soft signal only |
|------------|------------------|
| `hard_fail` from moral sermon | Mean score mid vs high |
| ban/glue spam | Missing every uneven “toy” |
| zero anchors on **long** prose | Not hitting 6.5 / 9+ |

Do not rewrite a readable balanced draft just to raise 6 → 9.

## Anti-templates

Avoid stacking these every draft:

- “I’m writing this after…”
- “Here’s the turn”
- “Aftermath isn’t X. It’s Y.”
- Forced multi-scene aftermath + twist + theme-4 on short prose
- Novel discourse toys on emails / bios / blurbs

## Prefer

- One deliberate **skip** (set up, don’t pay off)
- One **boring** true detail
- End on image / action / cutoff — not a moral restatement
- Fragments, contractions, interrupt when natural

## Genre notes

| Form | Note |
|------|------|
| Long fiction | open cost OK; greyer choice; skip tidy denouement if it would sermonize |
| Email | anchors + specific ask; no “hope this finds you well”; no novel toys |
| Bio | one real time/place; no passion-driven fluff |
| Marketing | one concrete scene beats “unlock growth” |
| Tech answer | timestamps, commands, failed path first |
