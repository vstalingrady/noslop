"""Structural honesty: skill pack ships paper + flow, not score-max as win."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "noslop"
README = ROOT / "README.md"
MODES = ROOT / "evals" / "results" / "modes"
SUMMARY = MODES / "SUMMARY.md"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def test_paper_one_pager_exists_and_states_construction():
    paper = SKILL / "paper.md"
    assert paper.is_file(), "skills/noslop/paper.md required"
    t = _read(paper).lower()
    assert "construction" in t or "discourse" in t
    assert "over-explain" in t or "over-explains" in t or "theme" in t
    assert "forge" in t
    assert "5,000" in t or "5000" in t or "5k" in t
    assert "2604.03136" in _read(paper)


def test_skill_ship_bar_not_score_max():
    skill = _read(SKILL / "SKILL.md")
    assert "Ship bar" in skill or "ship bar" in skill.lower()
    assert "balanced" in skill.lower()
    assert re.search(r"max\s*=\s*research|research only", skill, re.I)
    assert "paper.md" in skill
    # must not require P(human) >= 0.5 as ship
    assert "≥ 0.5" in skill or ">= 0.5" in skill or "P(human)" in skill
    low = skill.lower()
    assert "genre split" in low or "long fiction" in low
    assert "short agent" in low or "short agent prose" in low
    # score-max must be framed as fail / not win
    assert "score-max" in low or "maximize voice" in low or "do not maximize" in low


def test_skill_subject_is_not_method():
    """'Use noslop' must not become a story about scores/the tool."""
    skill = _read(SKILL / "SKILL.md")
    low = skill.lower()
    assert "subject" in low and "method" in low
    assert "how you write" in low or "how" in low
    # hijack / meta failure modes named
    assert "subject hijack" in low or "not the default what" in low or "never the default what" in low
    assert "subject:" in low  # PRE-WRITE field
    assert "subject check" in low
    # must not allow "analyze repo + story" → story about repo without explicit ask
    assert "analyze" in low and ("repo" in low or "project" in low)
    cl = _read(SKILL / "checklists.md").lower()
    assert "subject" in cl
    assert "method" in cl or "noslop/scores" in cl or "skill/score" in cl


def test_voice_docs_anti_glue_not_quality_ladder():
    v = _read(SKILL / "voice.md").lower()
    assert "anti-glue" in v or "soft" in v
    assert "not" in v and ("human quality" in v or "maximize" in v or "ladder" in v)


def test_human_coding_is_lab_only():
    h = _read(SKILL / "human_coding.md").lower()
    assert "lab" in h
    assert "not a ship" in h or "not ship" in h
    assert "forge" in h


def test_modes_md_balanced_default_max_research():
    m = _read(SKILL / "modes.md").lower()
    assert "default ship" in m or "ship default" in m or "default ship mode = balanced" in m
    assert "research" in m
    assert "failure" in m or "not the hero" in m


def test_readme_paper_no_undetectable_theater():
    r = _read(README)
    low = r.lower()
    assert "2604.03136" in r or "storyscope" in low
    assert "install" in low
    assert "undetectable" not in low
    assert "gptzero" not in low
    assert "balanced" in low
    # install section should appear (bottom-ish content exists)
    assert "Copy-Item" in r or "pip install" in r


def test_modes_drafts_distinguish_modest_and_max():
    """modest ≠ max: max arms carry research craft stamps; modest does not."""
    for brief in ("mall_shoe", "cold_email"):
        modest = _read(MODES / f"{brief}_modest.md")
        mx = _read(MODES / f"{brief}_max.md")
        bal = _read(MODES / f"{brief}_balanced.md")
        assert modest.strip() and mx.strip() and bal.strip()
        assert modest.strip() != mx.strip()
        # max intentionally uses craft-show stamps for research illustration
        stamps = ("here's the turn", "i'm writing", "aftermath")
        max_low = mx.lower()
        modest_low = modest.lower()
        assert any(s in max_low for s in stamps), f"{brief} max should show research stamps"
        assert not any(s in modest_low for s in stamps), f"{brief} modest must stay unforced"


def test_modes_summary_recommends_balanced_flow():
    s = _read(SUMMARY).lower()
    assert "balanced" in s
    assert "ship" in s
    assert "flow" in s or "readable" in s
    assert "max" in s and ("research" in s or "not" in s)


def test_voice_cli_path_still_scores_real_text():
    """Drive shipped voice scorer — not a reimplementation."""
    from noslop.voice import score_voice

    slop = (
        "I hope this email finds you well. In today's rapidly evolving landscape, "
        "we leverage cutting-edge solutions to unlock seamless outcomes. "
        "I used to think process mattered. Turns out it was about heart."
    )
    clean = (
        "Maya — Thursday 9–11 had six empty slots of fourteen. "
        "Jakarta hours. Shared sheet, three days. If noise, delete. — Raka"
    )
    r_slop = score_voice(slop)
    r_clean = score_voice(clean)
    assert r_slop["hard_fail"] is True or r_slop["score"] < r_clean["score"]
    assert r_clean["hard_fail"] is False
