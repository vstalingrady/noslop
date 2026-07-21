# noslop checklists

These are **scans to run over a draft**, not ingredients to put in one.
A scan that finds nothing changes nothing.

## PRE-WRITE (four lines)

Mental is fine for anything under ~300 words.

```text
Subject:   (piece topic/plot — not noslop/scores/skill unless user asked)
Audience:
Form / length:
Biggest risk for this piece:  (glue? sermon? over-craft? fog?)
```

Subject ≠ method: noslop is HOW you write. If Subject would be the
tool/scores/repo and the user didn't ask for that topic → stop, take a real
premise.

## Slop scan (all forms)

Run over the draft; cut what you find. Zero hits = done.

```text
Hard-ban words / phrases / openers:   0 hits
Template patterns (Not just X but Y…): 0 hits
Sermon / lesson close:                 none
Parataxis stack (short. short. short.): none
Rule-of-three default:                 none
Em-dash spam (~≤1/500w):               ok
Markdown-in-email / format leaks:      none
Invented stats/quotes/anecdotes:       none
```

Full lists + swaps: [style-and-bans.md](style-and-bans.md).

## Over-application scan (all forms)

Cut these too — they're the skill's own slop:

```text
Anchor stuffing (digits nobody needed):      none
Fragment cosplay (pronouns stripped):        none
Signature closer ("delete it", "No deck."):  none
Punchy moral one-liner as last beat:         none
Boring-detail theater / manufactured mess:   none
Same skeleton as your last noslop piece:     no
```

## Long fiction (only when structure sags)

Light PRE-STRUCTURE from [construction.md](construction.md) — pick 0–3 moves,
linear default, diversity seed = moves you deliberately skip. Never stack the
palette; never force a time jump. Empty palette + clean scans + a page that
reads = valid ship.

```text
Tidy lesson / TED close:            none
Forced moves that don't earn space: none
Synonym-only "FIX":                 not a fix
```

## Long nonfiction (~1k+ words — only when one register runs the whole piece)

Light PRE-DRAFT from [structure-nonfiction.md](structure-nonfiction.md) —
pick 2–4 palette moves, seed macro choices (order / omissions / stopping
points), name the skips. Detector checks are smoke tests: max one structural
re-pass, section level only, no paraphrase tools.

```text
Every section same shape:            no
Kicker/closing beat on every section: no
Zero restatement of any point:       no
Every raised question resolved:      no
One register held end to end:        no
Sentence-level score chasing:        never
```

## VOICE (optional)

```text
hard_fail flags: none   ← only this blocks ship
fragment_stacks ≥ 3: rewrite with pronouns
(lab) score: informational — never iterate to raise it
```

CLI: `python -m noslop.cli voice --text-file draft.md`
