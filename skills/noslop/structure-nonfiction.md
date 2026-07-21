# Nonfiction structure (long prose)

**Draft first. Open this file for long nonfiction (~1k+ words), or when a draft
reads like one sustained register.**
Sparse moves. Not a score recipe. Not a detector recipe.

Ship bar = a careful reader finishes the page without template nausea.
Detectors = smoke tests, footnotes only — never the win.

A draft that already reads well needs **zero** moves from this file.

## The diagnosis (why clean long nonfiction still trips detectors)

A draft can pass every surface ban and still read as machine. The tell is not
vocabulary — it is **evenness**: one register held for the whole piece, every
section built the same way, every thought closed, every sentence resolving at
the same rate, and the writer explaining what each fact means. Humans drift,
restate themselves, leave threads dangling, and write purely functional
sentences with no craft in them. Detectors key on the evenness, not the words.

## Flexibility (read this)

The palette is a **menu**, not a checklist.

- **Most drafts should leave most moves unused.** Pick **2–4** that serve the
  brief. Rest stay off.
- Same picks every draft = new template. **Diversity seed** = deliberately
  skip something, and name the skips.
- Seed the **macro choices** too: topic order, real omissions, stopping
  points. Predictable structure is the signal; unusual-but-honest choices are
  the fix, not unusual adjectives.
- A plain, linear, evenly-argued draft that reads well is still a valid ship.
  This file fixes sag and sameness; it does not manufacture mess.

## PRE-DRAFT (long nonfiction — keep it light)

```text
NONFICTION PRE-DRAFT
Subject:        (from the brief — never the tool/scores)
Audience:
Form / length:
Macro seed:     topic order (not the obvious one) | real omissions
                | which sections end without a closing beat
Palette picks (2–4, name them): …
Diversity seed: palette + macro choices I will NOT use (name them)
```

A minute of thought, not a ceremony.

## Sparse palette (menu — pick 2–4 or none)

1. **Register drift** — don't hold one voice or irony level end to end;
   narration, aside, and dry summary alternate unevenly.
2. **Uneven architecture** — sections built differently; at least one section
   ends with no closing beat at all.
3. **Unresolved threads** — raise one or two questions and leave them
   dangling, stated plainly.
4. **Restatement over paraphrase** — returning to a point may repeat it in the
   same words; freshness-per-sentence is a machine habit.
5. **Functional sentences** — some sentences only do work (cite, qualify, move
   on). No craft quota.
6. **Thought-length burstiness** — a three-sentence idea next to a
   twelve-sentence one, unsmoothed.
7. **Interpret less** — facts stand alone more often. The sentence explaining
   what a fact means is the one a detector flags first.

**Not featured at once.** Skip freely.

## Structural FIX (max 1 round — section level only)

| Symptom | Fix (structure) | Not a fix |
|---------|-----------------|-----------|
| Every section same shape | Rebuild two sections differently | Softer synonyms |
| Kicker on every section | Cut half the kickers; end flat | Punchier kickers |
| Zero restatement | Say it again where a human would | "Vary the wording" |
| All thoughts closed | Cut one resolution; leave it open | Hedge words |
| One sustained register | Rewrite one section drier or looser | Sprinkle fragments |

FIX = sentence-level chasing against a score → **FAIL** (score-maxxing).

## Detector clause

An AI-detector check is a **smoke test**, never a coach:

- Run it at most twice: once on the draft, once after a structural re-pass.
- Re-passes happen at **section level**, never sentence level.
- No paraphrase tools, no "humanizer" passes, no iterating to lower a number.
- Detectors disagree with each other and with themselves. Pick one, treat
  the result as noisy, and stop. A page that reads human with a bad score
  beats a farmed number with stiff craft.

## After structure (style is still required)

Structure does **not** replace surface hygiene:

1. Full style + bans pass — required ([style-and-bans.md](style-and-bans.md)).
2. VOICE hard fails only ([voice.md](voice.md)) — anti-glue floor, not a ladder.
3. Ship when a careful human would finish the page **and** the ban list is clean.

Skipping bans because "the structure is uneven enough" = FAIL.

## Short agent prose

**Do not use this file** for email, bio, blurb, short answers.
Flow + anti-glue + real anchors only. Long fiction uses
[construction.md](construction.md), not this file.

## Background: what detectors measure (lab notes)

One line each. These explain *why* the palette works; they are not ship gates.

- **GPTZero** (Adam et al., [arXiv:2602.13042](https://arxiv.org/abs/2602.13042)):
  hierarchical multi-task classifier, red-teamed against paraphrasing — so
  post-hoc word swaps don't move it; draft-time structure does.
- **Binoculars** (Hans et al., [arXiv:2401.12070](https://arxiv.org/abs/2401.12070)):
  scores token-level predictability — human text wins by making choices a
  model wouldn't predict (order, omissions, stopping points), not odd words.
- **StoryScope** (Russell et al., [arXiv:2604.03136](https://arxiv.org/abs/2604.03136)):
  discourse features alone separate AI fiction at 93% F1 with style removed —
  AI over-explains themes, closes every thread, clusters. Fiction features;
  the meta-lesson (construction outranks style) is what this file borrows.
- **Detector disagreement** (Alshammari & Rao, [arXiv:2507.17944](https://arxiv.org/abs/2507.17944)):
  automated "humanizers" half-work and vendors disagree wildly — one smoke
  test, never multi-detector chasing.
- **Excess vocabulary** (Kobak et al., [arXiv:2407.07004](https://arxiv.org/abs/2407.07004)):
  the lexical fingerprint — already owned by the ban list. Surface layer only.

```text
# detector side (three different machines)
gptzero(text)    = hierarchical_classifier(text)       # multi-level, paraphrase-robust
binoculars(text) = mean(token_surprisal(text))         # "would a model write this next?"
storyscope(text) = classify(discourse_features(text))  # theme-explain, tidiness, shape

# drafting side (this file) — move before generation, not after
draft_long_nonfiction(brief):
    chosen = pick_2_to_4(PALETTE); skipped = PALETTE - chosen   # name both
    macro  = seed(topic_order, omissions, stopping_points)
    text   = draft(brief, plainly)           # no checklist in hand
    text   = slop_scan(text)                 # lexical layer (existing)
    text   = overapplication_scan(text)      # noslop-tell layer (existing)
    text   = apply(chosen, text)             # section level only
    ship_if(careful_human_finishes(text))    # unchanged bar

detector_check(text):                        # smoke test, max 1 structural repass
    if score(text) < threshold: ship
    elif repasses == 0: apply(chosen, text, level=SECTION)
    else: report_honestly()                  # no farming, no humanizers
```
