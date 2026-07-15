# -*- coding: utf-8 -*-
"""
Plot default vs noslop VOICE scores (charts only — no text excerpts).

  $env:PYTHONPATH="src"
  .\.venv\Scripts\python.exe evals\plot_compare.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "evals" / "results" / "v2"
HUMAN = ROOT / "evals" / "results" / "human"
OUT = ROOT / "evals" / "results" / "figures"
BRIEFS = [
    "mall_shoe",
    "cold_email",
    "personal_bio",
    "saas_blurb",
    "agent_answer",
]
LABELS = {
    "mall_shoe": "mall shoe",
    "cold_email": "cold email",
    "personal_bio": "bio",
    "saas_blurb": "SaaS blurb",
    "agent_answer": "agent answer",
}


def load_voice(brief: str, arm: str) -> dict:
    p = V2 / f"{brief}_{arm}_voice.json"
    return json.loads(p.read_text(encoding="utf-8"))


def load_human_phuman() -> list[tuple[str, float]]:
    rows = []
    for p in sorted(HUMAN.glob("*_score.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        name = p.stem.replace("_score", "").replace("_", " ")
        rows.append((name, float(r.get("p_human", 0))))
    return rows


def load_storyscope_ab() -> list[tuple[str, float, float]] | None:
    base = ROOT / "evals" / "results"
    out = []
    for brief in BRIEFS:
        d = base / f"{brief}_default_score.json"
        n = base / f"{brief}_noslop_score.json"
        if not d.is_file() or not n.is_file():
            return None
        pd = json.loads(d.read_text(encoding="utf-8"))["p_human"]
        pn = json.loads(n.read_text(encoding="utf-8"))["p_human"]
        out.append((LABELS[brief], float(pd), float(pn)))
    return out


def style():
    plt.rcParams.update(
        {
            "figure.facecolor": "#0f1115",
            "axes.facecolor": "#161a22",
            "axes.edgecolor": "#3a4150",
            "axes.labelcolor": "#d6dbe6",
            "text.color": "#d6dbe6",
            "xtick.color": "#a8b0c0",
            "ytick.color": "#a8b0c0",
            "grid.color": "#2a3140",
            "grid.alpha": 0.6,
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
        }
    )


def plot_voice_bars(path: Path) -> None:
    defaults = [load_voice(b, "default")["score"] for b in BRIEFS]
    noslops = [load_voice(b, "noslop")["score"] for b in BRIEFS]
    labels = [LABELS[b] for b in BRIEFS]
    x = np.arange(len(labels))
    w = 0.36

    fig, ax = plt.subplots(figsize=(10, 5.2))
    b1 = ax.bar(x - w / 2, defaults, w, label="default", color="#6b7280", edgecolor="#9ca3af")
    b2 = ax.bar(x + w / 2, noslops, w, label="noslop", color="#3b82f6", edgecolor="#93c5fd")
    ax.axhline(6.5, color="#f59e0b", linestyle="--", linewidth=1.2, label="PASS 6.5")
    ax.set_ylabel("VOICE score (0–10)")
    ax.set_title("default vs noslop — VOICE scores by brief")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylim(0, 10.5)
    ax.grid(axis="y")
    ax.legend(frameon=False)
    for bars in (b1, b2):
        for rect in bars:
            h = rect.get_height()
            ax.annotate(
                f"{h:.1f}",
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                color="#e5e7eb",
            )
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_axis_heatmap(path: Path) -> None:
    axes_names = ["anchors", "uneven", "moral_close", "rhythm", "glue_bans"]
    row_labels = []
    mat = []
    for b in BRIEFS:
        for arm, tag in (("default", "default"), ("noslop", "noslop")):
            r = load_voice(b, arm)
            row_labels.append(f"{LABELS[b]} · {tag}")
            mat.append([r["axes"][a] for a in axes_names])
    mat = np.array(mat, dtype=float)

    fig, ax = plt.subplots(figsize=(8.5, 7))
    im = ax.imshow(mat, aspect="auto", cmap="Blues", vmin=0, vmax=2)
    ax.set_xticks(range(len(axes_names)))
    ax.set_xticklabels(axes_names, rotation=25, ha="right")
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels)
    ax.set_title("VOICE axes (0–2) — default vs noslop")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(
                j, i, f"{mat[i, j]:.0f}", ha="center", va="center", color="#0f172a", fontsize=8
            )
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label="axis score")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_delta(path: Path) -> None:
    deltas = []
    labels = []
    for b in BRIEFS:
        d = load_voice(b, "default")["score"]
        n = load_voice(b, "noslop")["score"]
        deltas.append(n - d)
        labels.append(LABELS[b])
    order = np.argsort(deltas)
    deltas = [deltas[i] for i in order]
    labels = [labels[i] for i in order]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = ["#22c55e" if d >= 1.5 else "#f59e0b" for d in deltas]
    ax.barh(labels, deltas, color=colors, edgecolor="#14532d")
    ax.axvline(1.5, color="#f59e0b", linestyle="--", linewidth=1.1, label="Δ ≥ 1.5")
    ax.set_xlabel("noslop − default (VOICE)")
    ax.set_title("Lift per brief")
    ax.grid(axis="x")
    ax.legend(frameon=False)
    for i, d in enumerate(deltas):
        ax.text(d + 0.08, i, f"+{d:.1f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_human_baseline(path: Path) -> None:
    humans = load_human_phuman()
    if not humans:
        return
    ab = load_storyscope_ab()
    names = [h[0] for h in humans]
    vals = [h[1] for h in humans]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    y = np.arange(len(names))
    ax.barh(y, vals, color="#a78bfa", edgecolor="#c4b5fd", label="book excerpt")
    if ab:
        mean_d = float(np.mean([a[1] for a in ab]))
        mean_n = float(np.mean([a[2] for a in ab]))
        ax.axvline(
            mean_d, color="#6b7280", linestyle=":", linewidth=1.5, label=f"mean default AI {mean_d:.2f}"
        )
        ax.axvline(
            mean_n, color="#3b82f6", linestyle="--", linewidth=1.5, label=f"mean noslop {mean_n:.2f}"
        )
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlabel("StoryScope P(human)")
    ax.set_title("Human books vs AI means (StoryScope — diagnostic)")
    ax.set_xlim(0, 1.0)
    ax.grid(axis="x")
    ax.legend(frameon=False, loc="lower right", fontsize=8)
    note = "High StoryScope ≠ literary. Books often score lower than noslop feature packs."
    ax.text(0.01, -0.18, note, transform=ax.transAxes, fontsize=8, color="#9ca3af")
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def plot_storyscope_if_any(path: Path) -> None:
    ab = load_storyscope_ab()
    if not ab:
        return
    labels = [a[0] for a in ab]
    d = [a[1] for a in ab]
    n = [a[2] for a in ab]
    x = np.arange(len(labels))
    w = 0.36
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - w / 2, d, w, label="default", color="#6b7280")
    ax.bar(x + w / 2, n, w, label="noslop", color="#8b5cf6")
    ax.axhline(0.13, color="#f472b6", linestyle="--", linewidth=1.1, label="books mean ~0.13")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylabel("P(human)")
    ax.set_ylim(0, 1.0)
    ax.set_title("StoryScope P(human) — diagnostic only")
    ax.grid(axis="y")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main() -> int:
    style()
    OUT.mkdir(parents=True, exist_ok=True)

    # drop old excerpt plots if present (excerpts are markdown quotes, not PNGs)
    for stale in OUT.glob("excerpts_*.png"):
        stale.unlink()

    plot_voice_bars(OUT / "voice_scores_default_vs_noslop.png")
    plot_delta(OUT / "voice_delta.png")
    plot_axis_heatmap(OUT / "voice_axes_heatmap.png")

    if load_storyscope_ab():
        plot_storyscope_if_any(OUT / "storyscope_default_vs_noslop.png")
        plot_human_baseline(OUT / "human_books_baseline.png")

    # figures/README.md is hand-maintained (chart embeds + quoted excerpts)
    print("wrote figures to", OUT)
    print("  (excerpts are markdown quotes in figures/README.md + root README.md)")
    for p in sorted(OUT.glob("*.png")):
        print(" ", p.name, f"({p.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
