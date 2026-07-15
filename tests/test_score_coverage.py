"""Coverage-aware scoring and feature templates."""

from __future__ import annotations

import json
from pathlib import Path

from noslop.score import score
from noslop.template import build_template, write_template


def test_sparse_fails_min_coverage():
    r = score(
        features={"SIT_MET_303": "4"},
        model_name="narrative",
        threshold=0.5,
        min_coverage=0.8,
    )
    assert r["coverage"] < 0.8
    assert r["gate"] == "fail"
    assert r.get("warning")
    assert "min_coverage" in (r["warning"] or "")


def test_coverage_reported_without_min():
    r = score(
        features={"SIT_MET_303": "4"},
        model_name="narrative",
        threshold=0.5,
    )
    assert "coverage" in r
    assert r["features_extracted"] >= 1
    assert r["features_expected"] > 1


def test_features_template_high_gain(tmp_path: Path):
    data = build_template("high-gain")
    assert data["pack"] == "high-gain"
    assert "PLT_MOR_007" in data["features"]
    assert "SIT_MET_303" in data["features"]
    assert data["features"]["PLT_MOR_007"] is None
    assert isinstance(data["allowed"]["PLT_MOR_007"], list)
    assert len(data["allowed"]["PLT_MOR_007"]) >= 1

    out = tmp_path / "tpl.json"
    write_template(out, pack="high-gain")
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert "features" in loaded
    assert "allowed" in loaded
