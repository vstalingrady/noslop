# noslop realign to StoryScope paper + human flow

> **For agentic workers:** Use executing-plans / subagent-driven-development as needed. Checkbox steps. **Commit + push** after coherent delivery when user expects GitHub sync.

**Goal:** Realign noslop with StoryScope’s actual thesis (discourse construction on fiction: less theme dump, greyer choices, messier time, diversity) and make **human readability** the ship bar — not max VOICE/StoryScope scores.

**Architecture:** Rewrite skill docs first (north star + modes + genre split). Soften VOICE as anti-glue only. Keep StoryScope CLI as lab tool. Refresh modes eval + DOCX narrative so “high score / low flow = fail” is explicit. README plain English.

**Tech Stack:** Markdown skill pack, existing voice CLI, optional score CLI, existing modes corpus + DOCX builder, git.

**Spec:** `docs/superpowers/specs/2026-07-16-noslop-realign-paper.md`  
**Paper:** arXiv:2604.03136 · https://github.com/jenna-russell/storyscope

---

## File map

| Path | Change |
|------|--------|
| `skills/noslop/SKILL.md` | Paper-aligned north star; genre split; score-max is fail |
| `skills/noslop/paper.md` | **Create** — 1-page paper findings for agents |
| `skills/noslop/modes.md` | Tie modes to paper + flow (not score ladders) |
| `skills/noslop/voice.md` | VOICE = anti-glue only; not “human quality” |
| `skills/noslop/human_coding.md` | Rewrite as lab notes from paper, not ship recipe |
| `skills/noslop/checklists.md` | PRE-WRITE: Mode + paper construction lines for fiction |
| `README.md` | What paper is / what we ship; modes; install bottom |
| `evals/results/modes/*` | Re-draft if needed so modest/balanced **flow** better than max |
| `evals/results/noslop_modes_comparison.docx` | Rebuild with paper thesis + flow recommendation |
| Mirror | `%USERPROFILE%\.claude\skills\noslop\` |

---

### Task 1: Paper one-pager for agents

**Files:** Create `skills/noslop/paper.md`

- [ ] **Step 1:** Write plain-English bullets:
  - Paper measures **construction**, not ban-lists
  - AI: over-explain themes, tidy single-track
  - Human: moral ambiguity, temporal complexity, diversity
  - Corpus ~5k-word stories
  - Features should be **extracted**, not forged
  - Binary is a **detector research** tool, not a writing coach that says maximize P(human)

- [ ] **Step 2:** Link from SKILL.md

---

### Task 2: Skill realign

**Files:** `SKILL.md`, `modes.md`, `voice.md`, `human_coding.md`, `checklists.md`

- [ ] **Step 1:** SKILL iron law:
  ```
  Ship bar: careful human finishes the page.
  Do not maximize VOICE or StoryScope at cost of flow.
  Mode default = balanced. max = research only.
  ```
- [ ] **Step 2:** Genre split section (long fiction vs short agent prose).
- [ ] **Step 3:** Fiction construction from paper (no theme dump, grey choice, time texture when length allows).
- [ ] **Step 4:** VOICE docs: hard fails for glue/sermon only; **no “must hit 6.5/9” as human quality**.
- [ ] **Step 5:** human_coding.md = optional lab / long-form only.
- [ ] **Step 6:** Mirror skill pack.

---

### Task 3: Eval honesty

**Files:** `evals/results/modes/*`, `evals/run_modes_compare.py`, DOCX builder

- [ ] **Step 1:** Re-read all 8 drafts; rewrite any arm that is score-farm staccato so **modest/balanced read better than max** to a human (even if VOICE numbers don’t rank that way).
- [ ] **Step 2:** Re-run `python evals/run_modes_compare.py` (real voice path); capture JSON under scratch.
- [ ] **Step 3:** Rebuild DOCX: problem = we lost the paper plot; table of modes; full quotes; recommendation **balanced**; note VOICE ≠ flow ranking.
- [ ] **Step 4:** Optional: one ~800–1500 word fiction sample under `evals/results/longform/` with **honest** lean feature fill + StoryScope score as **illustration only** (not ship bar). Skip if time — document skip.

---

### Task 4: README

- [ ] Plain English: what paper measured vs what skill ships.
- [ ] Modes short table.
- [ ] Link DOCX + modes SUMMARY.
- [ ] Install at bottom.
- [ ] No GPTZero failure theater; no “undetectable” claims either.

---

### Task 5: Verify + push

- [ ] Mirror equals repo on Mode + ship bar wording.
- [ ] `pytest tests/ -q` still green (no XGBoost retrain).
- [ ] DOCX extract contains problem / modes / full drafts / ship balanced.
- [ ] `git commit` + `git push origin main`.

---

## Verification plan

1. Skill: paper findings present; score-max not ship goal; balanced default.  
2. Modes drafts: human can tell modest ≠ max; balanced is readable.  
3. DOCX complete.  
4. README scannable.  
5. Remote main updated.

## Deviations

- max mode arms intentionally include craft stamps (“Here's the turn”, aftermath framing); VOICE may score **lower** than modest/balanced — intended (flow > number; max = research stiffness demo).
- Optional longform StoryScope sample under `evals/results/longform/`: **skipped** (documented in modes SUMMARY).
