# -*- coding: utf-8 -*-
"""Score mode drafts with real VOICE CLI path; write SUMMARY + scratch JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from noslop.voice import score_voice  # noqa: E402

RES = ROOT / "evals" / "results" / "modes"
SCRATCH = Path(r"C:\Users\vstal\AppData\Local\Temp\grok-goal-db7190bf0214\implementer\modes_voice")
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
        "# noslop modes — VOICE comparison",
        "",
        "Human flow over score maxing. Scored with `noslop.voice.score_voice` / CLI voice path.",
        "StoryScope optional: not run for this table (no forged features).",
        "",
        "## Scores",
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
        "## Recommendation",
        "",
        "- **Ship default intensity: balanced** — readable, anti-glue/sermon, not score-farm.",
        "- **modest** — natural letters / low-pressure notes.",
        "- **max** — research only; expect stiff craft when numbers climb.",
        "- **default** — control arm (slop), not a skill mode.",
        "",
        "High VOICE with unreadable prose = failure. Book-band StoryScope (~0.1–0.3) is OK when flow is good.",
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
