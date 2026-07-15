# -*- coding: utf-8 -*-
"""A/B default vs noslop-v2 on VOICE gate."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from noslop.voice import score_voice  # noqa: E402

RES = ROOT / "evals" / "results" / "v2"
OUT = ROOT / "evals" / "results" / "SUMMARY_V2.md"
SCRATCH = Path(r"C:\Users\vstal\AppData\Local\Temp\grok-goal-3f1b8f04ea9a\implementer")

BRIEFS = [
    "mall_shoe",
    "cold_email",
    "personal_bio",
    "saas_blurb",
    "agent_answer",
]


def body(text: str) -> str:
    return "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("#"))


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    rows = []
    for brief in BRIEFS:
        for arm in ("default", "noslop"):
            path = RES / f"{brief}_{arm}.md"
            text = body(path.read_text(encoding="utf-8"))
            r = score_voice(text)
            score_path = RES / f"{brief}_{arm}_voice.json"
            score_path.write_text(json.dumps(r, indent=2), encoding="utf-8")
            (SCRATCH / f"voice_{brief}_{arm}.json").write_text(
                json.dumps(r, indent=2), encoding="utf-8"
            )
            rows.append(
                {
                    "brief": brief,
                    "arm": arm,
                    "score": r["score"],
                    "gate": r["gate"],
                    "hard_fail": r["hard_fail"],
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                }
            )
            print(
                f"{brief:16} {arm:8} score={r['score']:.2f} "
                f"gate={r['gate']} hard={r['hard_fail']}"
            )

    by: dict = {}
    for row in rows:
        by.setdefault(row["brief"], {})[row["arm"]] = row

    n_ok = 0
    lines = [
        "# noslop VOICE A/B SUMMARY",
        "",
        "Primary gate: `python -m noslop.cli voice` (threshold 6.5, no hard_fail).",
        "StoryScope P(human) is **not** the ship gate. Books mean ~0.13 — see HUMAN_BASELINE.md.",
        "GPTZero: not run in this environment (optional; no undetectable claim).",
        "",
        "## Per-brief",
        "",
        "| Brief | default | noslop | delta | noslop>=6.5? | delta>=1.5? |",
        "|-------|---------|--------|-------|--------------|-------------|",
    ]
    for brief in BRIEFS:
        d = by[brief]["default"]
        n = by[brief]["noslop"]
        delta = n["score"] - d["score"]
        ok6 = n["score"] >= 6.5 and not n["hard_fail"]
        okd = delta >= 1.5
        if ok6 and okd:
            n_ok += 1
        lines.append(
            f"| {brief} | {d['score']:.2f} ({d['gate']}) | {n['score']:.2f} ({n['gate']}) | "
            f"{delta:+.2f} | {'YES' if ok6 else 'NO'} | {'YES' if okd else 'NO'} |"
        )

    lines += [
        "",
        "## Criteria",
        f"- noslop VOICE >= 6.5 and delta >= 1.5 on >=4/5: **{n_ok}/5** -> "
        f"**{'PASS' if n_ok >= 4 else 'FAIL'}**",
        "",
        "## Paths",
        "",
        "| Brief | Arm | Draft | Voice JSON |",
        "|-------|-----|-------|------------|",
    ]
    for brief in BRIEFS:
        for arm in ("default", "noslop"):
            r = by[brief][arm]
            lines.append(
                f"| {brief} | {arm} | `{r['path']}` | "
                f"`evals/results/v2/{brief}_{arm}_voice.json` |"
            )

    lines += [
        "",
        "## Flagship",
        "`evals/results/v2/sample_flagship.md` (same brief as mall_shoe noslop arm).",
        "",
        "## Skill",
        "VOICE primary in `skills/noslop/SKILL.md`; mirrored to `%USERPROFILE%\\.claude\\skills\\noslop\\`.",
        "XGBoost model not retrained.",
        "",
    ]
    lines += [
        "## Figures",
        "",
        "Run `python evals/plot_compare.py` → `evals/results/figures/`",
        "(bar chart, deltas, axis heatmap, excerpt panels, optional StoryScope/books).",
        "",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:20]))
    print(f"\nWROTE {OUT}  ok={n_ok}/5")
    return 0 if n_ok >= 4 else 1


if __name__ == "__main__":
    raise SystemExit(main())
