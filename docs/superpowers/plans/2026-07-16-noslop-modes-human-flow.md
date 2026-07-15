# noslop modes (modest → max) + human-flow DOCX

> **For agentic workers:** REQUIRED: execute task-by-task; commit + push after coherent change sets when user asked for delivery.

**Goal:** Stop maxing detectors/scorers as the only win. Add **modest / balanced / max** writing modes, generate comparable drafts, and ship a **DOCX** showing effects vs human-readable flow (book-band scores ~0.1–0.3 on StoryScope are OK).

**Architecture:** Skill modes + eval corpus + VOICE scores (+ optional StoryScope) + one Word report. Default ship intensity = **balanced**.

**Tech Stack:** Markdown skill, existing `noslop.cli voice`, optional `score`, `docx` (docx-js), optional matplotlib bars only.

**Spec:** `docs/superpowers/specs/2026-07-16-noslop-modes-human-flow.md`

---

## File map

| Path | Role |
|------|------|
| `skills/noslop/modes.md` | Mode definitions |
| `skills/noslop/SKILL.md` | Mode in PRE-WRITE; balanced default; max not hero |
| `skills/noslop/checklists.md` | Mode line in templates |
| `evals/results/modes/` | Drafts per brief×mode |
| `evals/run_modes_compare.py` | Score all modes → JSON + table |
| `evals/results/modes/SUMMARY.md` | Numbers |
| `evals/results/noslop_modes_comparison.docx` | Full report with quotes |
| `README.md` | Short “Modes” section |

---

### Task 1: Skill modes

- [ ] Create `modes.md`: modest / balanced / max (do, don’t, when to use, score expectations).
- [ ] PRE-WRITE adds `Mode: modest|balanced|max` (default balanced).
- [ ] Ship bar: **balanced** = readable + VOICE no hard_fail (do **not** require 9+).
- [ ] **max** = research only; skill says so.
- [ ] Mirror skill to `%USERPROFILE%\.claude\skills\noslop\`.

### Task 2: Corpus

- [ ] Briefs: `mall_shoe`, `cold_email` (reuse prompts).
- [ ] Arms: `default`, `modest`, `balanced`, `max` for each.
- [ ] Write drafts that **honestly** match mode (modest = human flow, not score farm; max = current max craft).

### Task 3: Score

- [ ] Run VOICE on every draft.
- [ ] Optional: honest lean StoryScope maps for 1 fiction arm per mode (no forge).
- [ ] Write `evals/results/modes/SUMMARY.md`.
- [ ] Optional bar chart: mode × VOICE (no text-in-PNG).

### Task 4: DOCX

- [ ] Build `evals/results/noslop_modes_comparison.docx` with:
  - Problem statement (high scores / low flow)
  - Mode table
  - Score tables
  - Full quoted drafts (code-style paragraphs or block text)
  - Recommendation
- [ ] Validate docx if tooling available.

### Task 5: README + push

- [ ] README: short Modes section; install stays bottom; no GPTZero failure theater.
- [ ] `git commit` + `git push origin main`.

---

## Verification

1. Skill files define three modes; default balanced.  
2. 2×4 drafts exist and are scored.  
3. DOCX opens and contains all mode texts + numbers.  
4. SUMMARY shows modest closer to “quiet human” than max.  
5. Remote main has the commit.

## Deviations

(append only when executing)
