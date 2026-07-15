"""Score A/B stories with local XGBoost using hand-mapped StoryScope features."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from noslop.score import score

# Features use real taxonomy IDs + allowed-ish values (normalized by encoder).
# WITH noslop skill: concrete, loose ends, less sermon, timed night, named anger/fear.
WITH = {
    "SIT_MET_303": 2,  # thematic explicitness low-moderate
    "SIT_MET_501": "no",  # narratorial thematic commentary
    "SIT_MET_102": "no",  # ending self-commentary
    "SIT_MET_002": "no direct address",
    "PLT_MOR_001": "implicit_moral_inferred_from_outcomes_and_tone",
    "PLT_THM_008": 3,
    "PLT_CON_007": "primarily_protagonist_choice",
    "PLT_STR_003": "no_significant_subplots",
    "PLT_THM_005": "partially_resolved (some progress but key tensions remain)",
    "PLT_MOR_002": "ambivalent_or_morally_mixed",
    "EVT_SCH_004": "open_or_ambiguously_unresolved",
    "EVT_SCH_011": "partial_arc",
    "EVT_CAU_001": "mixed_explicit_and_implicit",
    "TMP_ORD_001": "mostly_chronological_with_rare_flashbacks",
    "TMP_DUR_008": "4_exact_calendar_dates_and_clock_times",
    "TMP_DUR_009": 4,
    "REV_DIS_003": "2_minor_analepses_or_prologue_only",
    "REV_SUS_003": "partially_resolved",
    "AGENT_EMO_004": "yes",  # has named emotional beats in text path - binary may differ
    "SET_ATM_005": "3_moderate",
    "SIT_MET_008": "Primarily explicit named references (titles, authors, specific works)",
    "SIT_MET_202": ["explicit_named_reference_to_specific_texts_or_authors"],
    "PER_FOC_009": "1_none_or_very_subtle_value_judgments",
    "SIT_GEN_010": 2,
}

# WITHOUT skill: moral sermon, system essay, tidy thematic close, heavy mood setting
WITHOUT = {
    "SIT_MET_303": 5,
    "SIT_MET_501": "yes",
    "SIT_MET_102": "yes",
    "SIT_MET_002": "no direct address",
    "PLT_MOR_001": "explicit_didactic_moral_or_authorial_comment",
    "PLT_THM_008": 5,
    "PLT_CON_007": "mixed_choice_and_chance",
    "PLT_STR_003": "no_significant_subplots",
    "PLT_THM_005": "reframed/transcended (tension transformed into new understanding)",
    "PLT_MOR_002": "affirmative_heroic",
    "EVT_SCH_004": "resolved_through_internal_understanding_or_acceptance",
    "EVT_SCH_011": "full_arc_with_resolution",
    "EVT_CAU_001": "predominantly_explicit_causation",
    "TMP_ORD_001": "strictly_chronological",
    "TMP_DUR_008": "3_relative_day_and_duration_markers",
    "TMP_DUR_009": 3,
    "REV_DIS_003": "1_strictly_linear_no_frames",
    "REV_SUS_003": "fully_resolved",
    "SET_ATM_005": "5_lush_overdetermined",
    "SIT_MET_008": "Primarily implicit echoes (genres, archetypes, unnamed myths)",
    "PER_FOC_009": "5_morally_commentative_voice_dominates_the_narration",
    "SIT_GEN_010": 5,
}


def main() -> None:
    results = {}
    for name, feats in [("with_noslop", WITH), ("without_noslop", WITHOUT)]:
        out = score(features=feats, model_name="narrative")
        results[name] = out
        path = ROOT / "tests" / "ab" / f"{name}.features.json"
        path.write_text(json.dumps({"features": feats}, indent=2), encoding="utf-8")
        print(f"=== {name} ===")
        print(
            f"label={out['label']}  P(human)={out['p_human']:.4f}  "
            f"P(AI)={out['p_ai']:.4f}  gate={out['gate']}"
        )

    w = results["with_noslop"]["p_human"]
    wo = results["without_noslop"]["p_human"]
    print("---")
    print(f"delta P(human) with - without = {w - wo:+.4f}")
    if w > wo:
        print("result: noslop-conditioned draft scores MORE human under XGBoost gate")
    elif w < wo:
        print("result: noslop-conditioned draft scores LESS human under XGBoost gate")
    else:
        print("result: tie")


if __name__ == "__main__":
    main()
