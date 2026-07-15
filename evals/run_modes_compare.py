# -*- coding: utf-8 -*-
"""Score mode drafts with real VOICE CLI path; write SUMMARY + scratch JSON."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from noslop.voice import score_voice  # noqa: E402

RES = ROOT / "evals" / "results" / "modes"
_SCRATCH_ENV = os.environ.get("NOSLOP_SCRATCH")
SCRATCH = Path(
    _SCRATCH_ENV
    if _SCRATCH_ENV
    else r"C:\Users\vstal\AppData\Local\Temp\grok-goal-34f82acb64b7\implementer\modes_voice"
)
BRIEFS = ["mall_shoe", "cold_email"]
ARMS = ["default", "modest", "balanced", "max"]


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    rows = []
    for brief in BRIEFS:
        for arm in ARMS:
            path = RES / f"{brief}_{arm}.md"
            text = path.read_text(encoding="utf-8")
            r = score_voice(text)
            out = {
                "brief": brief,
                "mode": arm,
                "score": r["score"],
                "gate": r["gate"],
                "hard_fail": r["hard_fail"],
                "hard_reasons": r.get("hard_reasons", []),
                "axes": r["axes"],
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            }
            (RES / f"{brief}_{arm}_voice.json").write_text(
                json.dumps(out, indent=2), encoding="utf-8"
            )
            (SCRATCH / f"{brief}_{arm}.json").write_text(
                json.dumps(r, indent=2), encoding="utf-8"
            )
            rows.append(out)
            print(
                f"{brief:12} {arm:10} score={r['score']:.2f} "
                f"gate={r['gate']} hard={r['hard_fail']}"
            )

    lines = [
        "# noslop modes — flow over score (paper realign)",
        "",
        "StoryScope (arXiv:2604.03136) measured **discourse construction** on fiction,",
        "not “maximize this VOICE number.” Ship bar = careful human finishes the page.",
        "",
        "Scored with `noslop.voice.score_voice` / CLI voice path as **soft anti-glue only**.",
        "VOICE numbers are **not** a flow ranking. Read the drafts.",
        "StoryScope binary not run here (no forged features).",
        "",
        "## Scores (informative only)",
        "",
        "| Brief | default | modest | balanced | max |",
        "|-------|---------|--------|----------|-----|",
    ]
    for brief in BRIEFS:
        by = {r["mode"]: r for r in rows if r["brief"] == brief}
        lines.append(
            f"| {brief} | {by['default']['score']:.2f} | {by['modest']['score']:.2f} | "
            f"{by['balanced']['score']:.2f} | {by['max']['score']:.2f} |"
        )
    lines += [
        "",
        "## Gates (hard_fail)",
        "",
        "| Brief | default | modest | balanced | max |",
        "|-------|---------|--------|----------|-----|",
    ]
    for brief in BRIEFS:
        by = {r["mode"]: r for r in rows if r["brief"] == brief}
        def g(m: str) -> str:
            return "HARD" if by[m]["hard_fail"] else by[m]["gate"]
        lines.append(
            f"| {brief} | {g('default')} | {g('modest')} | {g('balanced')} | {g('max')} |"
        )
    lines += [
        "",
        "## Human-flow notes (primary judge)",
        "",
        "- **modest** — unforced; digression OK; fewest craft stamps.",
        "- **balanced** — **ship default**; readable; anti-glue/sermon; no arc-toy dump.",
        "- **max** — research only: frame/turn/aftermath stamps on purpose; stiffer; **not** product win even if VOICE is high.",
        "- **default** — control slop (glue + sermon).",
        "",
        "## Recommendation",
        "",
        "- **Ship: balanced.**",
        "- **modest** for natural letters / low pressure.",
        "- **max** only when labeled research / stress craft.",
        "- High VOICE + stiff craft = failure. Book-band StoryScope (~0.1–0.3) OK when flow is good.",
        "- Longform StoryScope illustration: **skipped** this cycle (optional; not ship bar).",
        "",
        "## Drafts",
        "",
    ]
    for brief in BRIEFS:
        for arm in ARMS:
            lines.append(f"- `{brief}_{arm}.md`")
    lines.append("")
    summary = RES / "SUMMARY.md"
    summary.write_text("\n".join(lines), encoding="utf-8")
    print(f"WROTE {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
