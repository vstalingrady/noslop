"""Build empty feature templates for agent fill."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from noslop.paths import ARTIFACTS, ENCODER_STATE_PATH, TAXONOMY_PATH, require_file
from noslop.taxonomy import Taxonomy
from noslop.encode import load_encoder_state


def _high_gain_ids() -> list[str]:
    path = ARTIFACTS / "human_coding_targets.json"
    if path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
        pack = data.get("high_gain_pack")
        if isinstance(pack, list) and pack:
            return [str(x) for x in pack]
    return []


def feature_ids_for_pack(pack: str = "high-gain") -> list[str]:
    enc = load_encoder_state(require_file(ENCODER_STATE_PATH))
    narrative = list(enc["feature_ids"]["narrative"])
    if pack == "all":
        return narrative
    if pack == "core":
        core = [
            "SIT_MET_303",
            "SIT_MET_501",
            "SIT_MET_102",
            "PLT_MOR_001",
            "PLT_THM_008",
            "PLT_CON_007",
            "PLT_THM_005",
            "PLT_STR_003",
            "EVT_SCH_004",
            "EVT_CAU_001",
            "TMP_ORD_001",
            "TMP_DUR_008",
            "REV_DIS_003",
            "REV_SUS_003",
            "SET_ATM_005",
            "PER_FOC_009",
            "SIT_GEN_010",
            "SIT_MET_008",
            "SIT_MET_002",
        ]
        return [i for i in core if i in set(narrative)]
    # high-gain default
    hg = _high_gain_ids()
    if not hg:
        return narrative[:45]
    return [i for i in hg if i in set(narrative)]


def build_template(pack: str = "high-gain") -> dict[str, Any]:
    tax = Taxonomy.from_json(require_file(TAXONOMY_PATH))
    fmap = tax.feature_map
    ids = feature_ids_for_pack(pack)
    features = {fid: None for fid in ids}
    allowed = {
        fid: list(fmap[fid].values) if fid in fmap else []
        for fid in ids
    }
    return {
        "pack": pack,
        "features": features,
        "allowed": allowed,
    }


def write_template(out: Path, pack: str = "high-gain") -> Path:
    data = build_template(pack)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return out
