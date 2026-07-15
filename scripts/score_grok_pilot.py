"""Score Grok pilot: 5 with noslop vs 5 without. Local metrics only."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "docs" / "data" / "grok_pilot"
OUT_CSV = ROOT / "docs" / "data" / "grok_pilot_results.csv"

BANNED = [
    r"\bdelve\b",
    r"\btapestry\b",
    r"\brealm\b",
    r"\blandscape\b",
    r"\btestament\b",
    r"\bpivotal\b",
    r"\bintricate\b",
    r"\bmeticulous(?:ly)?\b",
    r"\bleverage\b",
    r"\bmultifaceted\b",
    r"\bseamless(?:ly)?\b",
    r"\brobust\b",
    r"\bgroundbreaking\b",
    r"\bcutting-edge\b",
    r"\bgame-?changer\b",
    r"\btransformative\b",
    r"\bparadigm\b",
    r"\bholistic\b",
    r"\bunderscore[sd]?\b",
    r"\bnavigat(?:e|ing)\b",
    r"\bunlock(?:ing)?\b",
    r"\bembark(?:ed)?\b",
    r"\bprofound\b",
    r"\bparamount\b",
    r"it's worth noting",
    r"it is worth noting",
    r"it is important to note",
    r"in today's",
    r"at its core",
    r"at the end of the day",
    r"the bottom line",
    r"here's the thing",
    r"here's the kicker",
    r"in a world where",
    r"in conclusion",
    r"\bmoreover\b",
    r"\bfurthermore\b",
    r"\badditionally\b",
    r"\bultimately\b",
    r"\boverall\b",
    r"not just .*[—-] it's",
    r"it's not just",
    r"care is not only",
    r"great question",
]

SERMON = [
    r"care is not only",
    r"the real (work|lesson|truth)",
    r"that is (the|what) (lesson|mattered|profound)",
    r"violence dressed as mercy",
    r"hospitals (do not only heal|author)",
    r"profound (lesson|realization|truth|affirmation)",
    r"what this means",
    r"the lesson",
]


def body_only(text: str) -> str:
    # strip PRE-WRITE / GRADE for surface metrics on prose
    t = re.sub(r"NOSLOP PRE-WRITE[\s\S]*?(?=\n\n[A-Z]|\nRina|\nRain|\nI wrote|\nThe ampoule|\nClipboard)", "", text, count=1)
    t = re.sub(r"\nNOSLOP GRADE[\s\S]*$", "", t)
    return t.strip()


def count_patterns(text: str, patterns: list[str]) -> int:
    n = 0
    low = text.lower()
    for p in patterns:
        n += len(re.findall(p, low, flags=re.I))
    return n


def sentence_cv(text: str) -> float:
    parts = re.split(r"[.!?]+", text)
    lens = [len(p.split()) for p in parts if p.strip()]
    if len(lens) < 2:
        return 0.0
    mean = sum(lens) / len(lens)
    if mean == 0:
        return 0.0
    var = sum((x - mean) ** 2 for x in lens) / len(lens)
    return (var**0.5) / mean


def skill_flags(raw: str) -> dict:
    return {
        "has_prewrite": "NOSLOP PRE-WRITE" in raw,
        "has_grade": "NOSLOP GRADE" in raw,
        "has_merged": bool(re.search(r"MERGED:\s*PASS", raw)),
    }


def score_file(path: Path, condition: str) -> dict:
    raw = path.read_text(encoding="utf-8")
    prose = body_only(raw) if condition == "with" else raw
    words = max(1, len(prose.split()))
    em = prose.count("—") + prose.count("–") + prose.count("--")
    flags = skill_flags(raw) if condition == "with" else {
        "has_prewrite": False,
        "has_grade": False,
        "has_merged": False,
    }
    return {
        "file": path.name,
        "condition": condition,
        "words": words,
        "banned_hits": count_patterns(prose, BANNED),
        "sermon_hits": count_patterns(prose, SERMON),
        "em_dash_per_1k": round(1000 * em / words, 2),
        "sentence_cv": round(sentence_cv(prose), 3),
        **flags,
    }


def main() -> None:
    rows = []
    for cond, sub in [("without", "without"), ("with", "with")]:
        d = PILOT / sub
        for p in sorted(d.glob("run*.txt")):
            rows.append(score_file(p, cond))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    def avg(cond: str, key: str) -> float:
        xs = [r[key] for r in rows if r["condition"] == cond]
        return sum(xs) / len(xs)

    print("=== Grok pilot: 5 with noslop vs 5 without ===\n")
    print(f"{'file':12} {'cond':8} {'banned':>6} {'sermon':>6} {'em/1k':>6} {'sent_cv':>7} {'PRE':>4} {'GRADE':>5} {'PASS':>4}")
    for r in rows:
        print(
            f"{r['file']:12} {r['condition']:8} {r['banned_hits']:6} {r['sermon_hits']:6} "
            f"{r['em_dash_per_1k']:6.1f} {r['sentence_cv']:7.3f} "
            f"{str(r['has_prewrite'])[:1]:>4} {str(r['has_grade'])[:1]:>5} {str(r['has_merged'])[:1]:>4}"
        )

    print("\n=== Means ===")
    for cond in ("without", "with"):
        print(
            f"{cond:8}  banned={avg(cond,'banned_hits'):.1f}  "
            f"sermon={avg(cond,'sermon_hits'):.1f}  "
            f"em/1k={avg(cond,'em_dash_per_1k'):.1f}  "
            f"sent_cv={avg(cond,'sentence_cv'):.3f}"
        )
    print(
        f"\nSkill compliance (with only): "
        f"PRE-WRITE {sum(r['has_prewrite'] for r in rows if r['condition']=='with')}/5  "
        f"GRADE {sum(r['has_grade'] for r in rows if r['condition']=='with')}/5  "
        f"MERGED PASS {sum(r['has_merged'] for r in rows if r['condition']=='with')}/5"
    )
    print(f"\nCSV → {OUT_CSV}")


if __name__ == "__main__":
    main()
