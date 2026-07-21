# Nonfiction Structure Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a general long-nonfiction structural layer to noslop so long essays stop carrying the evenness detectors key on, without score-chasing — plus a README refresh with reference papers and diagrams, and a clean-context 1k-word A/B validation pair.

**Architecture:** noslop already owns the lexical layer (style-and-bans.md) and a fiction structure layer (construction.md). This plan adds the missing third layer: general, draft-time structural principles for long nonfiction, grounded in five detection papers, with a strict anti-score-maxxing detector clause. Validation is done by two fresh-context subagents (control vs. treatment), not by the planner's contaminated context.

**Tech Stack:** Markdown skill files, pytest (structural-honesty tests), mermaid diagrams in README, PowerShell install step.

## Global Constraints

- Rules stay **general**; no banned-construction lists (a list of banned shapes is the same failure one level up).
- Detector checks = smoke test, **max 1 structural re-pass, section level only**, one detector, no paraphrase/"humanizer" tools.
- `tests/test_skill_realign.py` must stay green — SKILL.md edits must keep asserted strings ("genre split", "long fiction", "short agent", "balanced", "research only", "P(human)").
- README keeps the no-evasion-marketing ethos: detector papers may be **cited**, claims like "pass/beat/bypass" are banned (test relaxed accordingly, nothing else).
- Repo is source of truth (`C:\Users\vstal\noslop`); install = Copy-Item to `~/.claude/skills/noslop/`.
- One commit at the end, per user instruction (overrides frequent-commits default).

## Background: papers → restatement → counter

| Paper | What it does | Restated | Counter (in structure-nonfiction.md) |
|---|---|---|---|
| GPTZero (arXiv:2602.13042) | Hierarchical multi-task classifier, red-teamed vs paraphrase | Learned what AI text *is* at several levels; survives synonym swaps | Build differently at draft time; no post-hoc tricks |
| Binoculars (arXiv:2401.12070) | Token-level surprisal, cross-model | "Would a model write this next?" Humans keep surprising it | Macro seed: topic order, real omissions, early stops |
| StoryScope (arXiv:2604.03136) | 304 discourse features, 93% F1 style-free; AI over-explains, tidies, clusters | Even word-stripped, AI drafts share one tidy shape | Interpret less; unresolved threads; diversity seed |
| Alshammari & Rao (arXiv:2507.17944) | Humanizer attacks half-work; detectors disagree | Evasion tooling is dice; vendors don't agree | One smoke test; never multi-detector chasing |
| Kobak et al. (arXiv:2407.07004) | Excess-vocabulary fingerprint | The "delve" layer | Already owned by style-and-bans.md |

```text
# detector side (three machines)
gptzero(text)    = hierarchical_classifier(text)
binoculars(text) = mean(token_surprisal(text))
storyscope(text) = classify(discourse_features(text))

# drafting side — move before generation, not after
draft_long_nonfiction(brief):
    chosen = pick_2_to_4(PALETTE); skipped = PALETTE - chosen
    macro  = seed(topic_order, omissions, stopping_points)
    text   = draft(brief, plainly)
    text   = slop_scan(text)              # lexical layer (existing)
    text   = overapplication_scan(text)   # noslop-tell layer (existing)
    text   = apply(chosen, text)          # section level only
    ship_if(careful_human_finishes(text))

detector_check(text):                     # smoke test, max 1 structural repass
    if score(text) < threshold: ship
    elif repasses == 0: apply(chosen, text, level=SECTION)
    else: report_honestly()
```

---

### Task 1: Create `skills/noslop/structure-nonfiction.md`

**Files:**
- Create: `skills/noslop/structure-nonfiction.md`

**Produces:** the nonfiction layer other tasks point at.

- [x] **Step 1:** Write the file — diagnosis (evenness), flexibility block (menu not checklist), NONFICTION PRE-DRAFT block, 7-principle sparse palette (register drift / uneven architecture / unresolved threads / restatement / functional sentences / thought-length burstiness / interpret less), structural FIX table (max 1 round, section level), detector clause, after-structure note, background section (5 papers + pseudocode above).
- [x] **Step 2:** Verify idiom matches construction.md (ship bar, "menu, not a checklist", diversity seed, "Not featured at once").

### Task 2: Route long nonfiction in `SKILL.md`

**Files:**
- Modify: `skills/noslop/SKILL.md` (workflow step 5, genre-split table, Refs line)

- [x] **Step 1:** Step 5 → LONG PROSE ONLY, fiction → construction.md, nonfiction → structure-nonfiction.md. Keep "linear + plain is a valid ship".
- [x] **Step 2:** Add Long nonfiction row to genre-split table (keep Long fiction and Short agent prose rows verbatim).
- [x] **Step 3:** Add structure-nonfiction.md to Refs line.

### Task 3: Long-nonfiction scan in `checklists.md`

**Files:**
- Modify: `skills/noslop/checklists.md`

- [x] **Step 1:** Add "Long nonfiction" scan block after the Long fiction block: same-shape sections? kicker on every section? zero restatement? everything resolved? one register? sentence-level score chasing: never.

### Task 4: Rewrite `README.md`

**Files:**
- Modify: `README.md`

**Consumes:** Task 1 file paths. **Produces:** public docs with papers + diagrams.

- [x] **Step 1:** Rewrite: keep logo, A/B examples, modes, VOICE table, install, license. Add "evenness problem" section (craft language), 2 mermaid diagrams (detector mechanisms per papers; noslop pipeline), Reference papers table (5 papers, one line each), npx install line (`npx skills add vstalingrady/noslop`, repo is public).
- [x] **Step 2:** Keep test-asserted strings: "2604.03136", "install", "balanced", "Copy-Item". No "undetectable", no "pass/beat/bypass/fool" claims.

### Task 5: Relax `test_readme_paper_no_undetectable_theater`

**Files:**
- Modify: `tests/test_skill_realign.py:82-91`

- [x] **Step 1:** Replace `"gptzero" not in low` with a list of banned evasion *claims* ("pass gptzero", "beat gptzero", "bypass gptzero", "fool gptzero", "pass/beat/bypass ai detection", "fool detectors", "evade detection"). Keep "undetectable" ban and all other asserts.

### Task 6: Test suite green

- [ ] **Step 1:** Run: `.\.venv\Scripts\python.exe -m pytest tests -q` (fallback: `python -m pytest tests -q`). Expected: all pass.

### Task 7: Install skill

- [ ] **Step 1:** Run: `Copy-Item -Force .\skills\noslop\* $env:USERPROFILE\.claude\skills\noslop\`

### Task 8: Clean-context A/B pair (c8, 1k words)

**Files:**
- Create: `evals/results/longform/c8_default.md`, `evals/results/longform/c8_nonfiction.md`
- Modify: `evals/results/longform/README.md` (c8 row)

**Design:** c8 = first nonfiction eval pair, same brief, ~1,000 words each. Two fresh subagents: CONTROL gets the bare brief only; TREATMENT gets the brief + pointer to read `skills/noslop/` and follow the skill. Neither sees the detector report or this conversation — the planner's context is fitted to the report and would prove nothing. User runs GPTZero on both files afterward (smoke test).

- [ ] **Step 1:** Dispatch both subagents in parallel.
- [ ] **Step 2:** Save outputs as c8_default.md / c8_nonfiction.md; add c8 row + how-to-judge note to longform README.
- [ ] **Step 3:** Report file paths to user for the GPTZero run. <20% treatment ships; 20–40% = one structural re-pass (new clean subagent, section level); beyond that, stop and report honestly.

### Task 9: Single commit

- [ ] **Step 1:** Stage only this task's files (README.md, skills/noslop/SKILL.md, checklists.md, structure-nonfiction.md, tests/test_skill_realign.py, docs/superpowers/plans/this file, evals/results/longform/c8_* + README). Leave pre-existing unrelated modifications and untracked `mcps/` for user review.
- [ ] **Step 2:** `git commit -m "feat: add long-nonfiction structure layer, README papers+diagrams, c8 eval pair"`

## Self-review notes

- Spec coverage: general rules ✓ (Task 1), keep style ✓ (palette is draft-time, not polish), no score-maxxing ✓ (detector clause), README papers+diagrams ✓ (Task 4), clean-context A/B ✓ (Task 8), 1k words ✓ (Task 8), single commit ✓ (Task 9).
- GPTZero target is a user-run gate; no task promises a number.
