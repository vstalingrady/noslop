# noslop

<p align="center">
  <img src="assets/logo.jpg" alt="noslop logo" width="140" />
</p>

<p align="center"><b>An agent skill for prose that doesn’t read like template AI.</b><br/>
Grounded in StoryScope’s findings on <i>how</i> stories are built — not score maxing.</p>

---

## What the paper measured

[StoryScope](https://arxiv.org/abs/2604.03136) (Russell et al., arXiv:2604.03136) compared human vs AI **fiction** on discourse-level **narrative construction** (~5k-word parallel stories): theme explanation, plot tidy-ness, moral ambiguity, time structure, diversity in narrative space.

| Paper finding (short) | What that means for writing |
|----------------------|-----------------------------|
| AI over-explains themes, tidy single-track plots | Don’t end with a TED moral; leave greyer costs |
| Humans more temporally complex / diverse | When length allows, messier time & choices OK |
| Style tells are easy to edit away | Construction is harder to fake with polish |

**noslop is not** “beat a detector” or “hit P(human) ≥ 0.5.”  
**noslop is** write so a careful human finishes the page — using paper construction on **long fiction**, and flow + anti-glue on **short agent prose**.

Paper one-pager for agents: [`skills/noslop/paper.md`](skills/noslop/paper.md)

---

## Ship bar

```
Careful human finishes the page without fatigue or “this is a template” nausea.
Do not maximize VOICE or StoryScope at the cost of flow.
Default mode = balanced. max = research only.
```

| Form | Rules |
|------|--------|
| Long fiction | Less theme dump; greyer choice; time texture when length allows |
| Short email / bio / blurb / answer | Flow + anti-glue + real anchors — **no** novel toys |

---

## Modes

| Mode | Point |
|------|--------|
| **modest** | Natural flow; light skill |
| **balanced** | **Ship default** — readable, anti-glue/sermon, not score-farm |
| **max** | Research only — full craft pressure; readability cost |
| *default* (evals) | Control arm: raw model slop |

Details: [`skills/noslop/modes.md`](skills/noslop/modes.md)  
Side-by-side report: [`evals/results/noslop_modes_comparison.docx`](evals/results/noslop_modes_comparison.docx) · [`evals/results/modes/SUMMARY.md`](evals/results/modes/SUMMARY.md)

---

## Example (same brief, readable ship vs slop)

### Cold email — control (slop)

```text
I hope this email finds you well. In today's rapidly evolving healthcare
landscape, we leverage cutting-edge analytics to unlock actionable insights...
```

### Cold email — balanced (ship)

```text
Subject: Thursday morning empties vs your monthly average

Maya —

Friend at a two-site clinic sent a stripped booking export. One Thursday
block: fourteen slots, six empty. Monthly average still looked polite (~18%).

I fix that kind of mismatch. Jakarta hours. Shared sheet, a few days.

If useful, reply with any ugly Tuesday CSV.
If noise, delete.

— Raka
```

More mode arms (modest / balanced / max): [`evals/results/modes/`](evals/results/modes/)

---

## How the skill works

```text
brief → PRE-WRITE (mode + genre) → draft → hard-fail check → ship if page flows
         optional lab: StoryScope feature score (never ship gate)
```

1. **PRE-WRITE** — mode, anchors, one mess, what *not* to force  
2. **Draft** — fiction construction **or** short-prose flow (genre split)  
3. **VOICE** — soft anti-glue; block only on sermon / ban spam / zero anchors on long text  
4. **Bans** — surface cleanup (`style-and-bans.md`)  
5. **StoryScope** — lab only if asked; honest labels; never forge  

Skill pack: [`skills/noslop/`](skills/noslop/)

---

## Two tools (don’t mix them up)

| Tool | Answers | Ship? |
|------|---------|-------|
| **VOICE** | Obvious glue / sermon / fog? | Soft anti-glue (hard fails only) |
| **StoryScope** | Feature map vs research binary? | Lab only — books often ~0.13 P(human) |

Book baseline notes: [`evals/results/HUMAN_BASELINE.md`](evals/results/HUMAN_BASELINE.md)

---

## Repo layout

```
noslop/
  assets/logo.jpg
  skills/noslop/           # install this into your agent
  src/noslop/              # voice + optional StoryScope CLI
  artifacts/               # taxonomy + model weights (no retrain this cycle)
  evals/results/modes/     # mode comparison drafts
  tests/
```

---

## Install

### 1. Skill (Claude Code / similar)

```powershell
Copy-Item -Force .\skills\noslop\* $env:USERPROFILE\.claude\skills\noslop\
```

Then:

```
/noslop
Write a short cold email about X.
```

### 2. Local CLI (optional)

```powershell
cd C:\path\to\noslop
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
$env:PYTHONPATH="src"

.\.venv\Scripts\python.exe -m noslop.cli voice --text-file draft.md --json
# research only:
.\.venv\Scripts\python.exe -m noslop.cli score --features features.json --json
```

---

## License

MIT. StoryScope notices: [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).  
Paper: [arXiv:2604.03136](https://arxiv.org/abs/2604.03136).
