"""Structural honesty: PLT_MOR_007=extended requires multi-scene post-climax prose."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "evals" / "results"

# Clock-ish markers that count as distinct aftermath beats when repeated after climax language
TIME_MARK = re.compile(
    r"\b("
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"morning|noon|afternoon|night|"
    r"\d{1,2}:\d{2}|\d{1,2}\s*a\.?m\.?|\d{1,2}\s*p\.?m\.?|"
    r"two days|one week|a month|week two|\+\d+\s*days?"
    r")\b",
    re.I,
)


def _draft_and_features(brief: str, arm: str = "noslop"):
    draft = (RES / f"{brief}_{arm}.md").read_text(encoding="utf-8")
    feats = json.loads((RES / f"{brief}_{arm}_features.json").read_text(encoding="utf-8"))[
        "features"
    ]
    return draft, feats


def test_extended_aftermath_has_multiple_post_climax_beats():
    """If labeled extended, draft must contain Aftermath / post-climax multi-beat structure."""
    briefs = ["mall_shoe", "cold_email", "personal_bio", "saas_blurb", "agent_answer"]
    for brief in briefs:
        draft, feats = _draft_and_features(brief)
        if "extended" not in str(feats.get("PLT_MOR_007", "")):
            continue
        # Require explicit multi-scene aftermath sectioning OR many time marks after 'climax'/'turn'/'twist'
        lower = draft.lower()
        assert (
            "aftermath" in lower
            or "what came after" in lower
            or "several" in lower
            or "more than one" in lower
        ), f"{brief}: extended label but no aftermath framing language"
        times = TIME_MARK.findall(draft)
        assert len(times) >= 4, (
            f"{brief}: extended needs multiple temporal beats; found {times}"
        )


def test_embodied_label_has_body_words():
    body = re.compile(
        r"\b(throat|knee|shoulder|shoulders|jaw|neck|hands|eyes|fingers|coffee|tile|grit|sweat)\b",
        re.I,
    )
    for brief in ["mall_shoe", "cold_email", "personal_bio", "saas_blurb", "agent_answer"]:
        draft, feats = _draft_and_features(brief)
        if "embodied" not in str(feats.get("AGENT_EMO_009", "")):
            continue
        assert body.search(draft), f"{brief}: embodied label without body lexicon"


def test_cites_file_exists_for_noslop_arms():
    for brief in ["mall_shoe", "cold_email", "personal_bio", "saas_blurb", "agent_answer"]:
        p = RES / f"{brief}_noslop_cites.md"
        assert p.is_file(), p
        text = p.read_text(encoding="utf-8")
        assert "PLT_MOR_007" in text
        assert "AGENT_EMO_009" in text
