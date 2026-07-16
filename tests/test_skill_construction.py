"""Skill pack encodes StoryScope-aligned construction, not score-farm."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "noslop"


def _read(name: str) -> str:
    return (SKILL / name).read_text(encoding="utf-8").lower()


def test_construction_md_exists():
    assert (SKILL / "construction.md").is_file(), "skills/noslop/construction.md required"


def test_construction_has_pre_structure_and_diversity_seed():
    t = _read("construction.md")
    assert "pre-structure" in t or "pre_structure" in t
    assert "diversity seed" in t or "diversity_seed" in t
    assert "sparse" in t or "2–4" in t or "2-4" in t


def test_construction_has_length_gates():
    t = _read("construction.md")
    assert "length" in t
    assert "short" in t and ("fiction" in t or "long" in t)


def test_construction_has_structural_fix_not_synonym():
    t = _read("construction.md")
    assert "fix" in t
    assert "synonym" in t or "not a fix" in t
    assert "structure" in t


def test_skill_links_construction_and_structure_first():
    skill = _read("SKILL.md")
    assert "construction.md" in skill
    assert "structure" in skill
    assert "diversity" in skill
    # long fiction: structure before draft
    assert "pre-structure" in skill or "pre_structure" in skill


def test_skill_anti_scoremax_ship_bar():
    skill = _read("SKILL.md")
    assert "score-max" in skill or "scoremax" in skill or "do not maximize" in skill
    assert "careful human" in skill or "careful reader" in skill or "finishes the page" in skill
    # high scores must not be framed as win alone
    assert "stiff" in skill or "fail even if" in skill or "not ship bar" in skill or "footnote" in skill


def test_paper_warns_against_inverting_detector():
    p = _read("paper.md")
    assert "invert" in p or "must-hit" in p or "cluster" in p
    assert "generator" in p or "sparse" in p or "diversity" in p


def test_checklists_include_fiction_pre_structure_fields():
    c = _read("checklists.md")
    assert "diversity" in c or "pre-structure" in c or "time shape" in c or "ending type" in c
    assert "construction.md" in c or "pre-structure" in c


def test_short_prose_still_forbids_novel_toys():
    skill = _read("SKILL.md")
    assert "novel toy" in skill or "novel toys" in skill
    assert "short agent" in skill
