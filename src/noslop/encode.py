"""
Feature encoding for StoryScope taxonomy values.

Paper (arXiv:2604.03136): one-hot categorical, multi-hot multi-select,
numeric ordinal/scale, binary as 0/1.

Upstream released .json weights were trained with an unpublished column layout
(954 / 1104 dims). We freeze our layout in encoder_state.json and train
matching XGBoost weights with the paper's hyperparameters so inference is exact
for *this* encoding of the *same* 304 features / same data.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import numpy as np

from noslop.taxonomy import Taxonomy, best_match, normalize_str


def _to_list_atoms(raw: Any) -> list[str]:
    if raw is None or raw == "" or raw == "n/a":
        return []
    if isinstance(raw, list):
        return [str(x) for x in raw]
    return [p.strip() for p in str(raw).split("|") if p.strip()]


def build_column_plan(tax: Taxonomy, feature_ids: list[str]) -> list[dict[str, Any]]:
    """Deterministic column plan from taxonomy alone (no training scan)."""
    fmap = tax.feature_map
    plan: list[dict[str, Any]] = []
    for fid in feature_ids:
        f = fmap[fid]
        if f.type == "categorical":
            for val in f.values:
                plan.append(
                    {"kind": "onehot", "feature_id": fid, "value": val, "name": f"{fid}__{val}"}
                )
        elif f.type == "multi_select":
            for val in f.values:
                plan.append(
                    {
                        "kind": "multi_hot",
                        "feature_id": fid,
                        "value": val,
                        "name": f"{fid}__{val}",
                    }
                )
        elif f.type == "binary":
            # 0/1 from first/second taxonomy value or yes/no
            plan.append({"kind": "binary", "feature_id": fid, "values": f.values, "name": fid})
        elif f.type == "ordinal":
            plan.append(
                {"kind": "ordinal", "feature_id": fid, "values": f.values, "name": fid}
            )
        elif f.type == "scale":
            plan.append({"kind": "scale", "feature_id": fid, "name": fid})
        else:
            plan.append({"kind": "scale", "feature_id": fid, "name": fid})
    return plan


def encode_row(
    features: dict[str, Any],
    plan: list[dict[str, Any]],
    tax: Taxonomy | None = None,
) -> np.ndarray:
    fmap = tax.feature_map if tax is not None else {}
    vec: list[float] = []

    for col in plan:
        fid = col["feature_id"]
        raw = features.get(fid, None)
        kind = col["kind"]

        if kind == "onehot":
            val = col["value"]
            s = "__MISSING__" if raw is None or raw == "" else str(raw)
            if tax is not None and fid in fmap and s not in ("__MISSING__", "n/a"):
                s = best_match(s, fmap[fid].values)
            vec.append(1.0 if s == val or normalize_str(s) == normalize_str(val) else 0.0)

        elif kind == "multi_hot":
            val = col["value"]
            atoms = _to_list_atoms(raw)
            if tax is not None and fid in fmap:
                atoms = [best_match(a, fmap[fid].values) for a in atoms]
            norms = {normalize_str(a) for a in atoms}
            hit = normalize_str(val) in norms or val in atoms
            vec.append(1.0 if hit else 0.0)

        elif kind == "binary":
            s = str(raw).strip().lower() if raw is not None else ""
            # positive if yes/present/true or second-ish positive tokens
            pos = s in ("yes", "true", "1", "present") or s.startswith("yes")
            if not pos and col.get("values"):
                # last value often the "present" option in this taxonomy — use yes-like match
                pos = s == str(col["values"][-1]).strip().lower()
                # better: explicit yes/no pairs
                for v in col["values"]:
                    vl = str(v).lower()
                    if s == vl and any(p in vl for p in ("yes", "present", "true")):
                        pos = True
            vec.append(1.0 if pos else 0.0)

        elif kind == "ordinal":
            values = col.get("values") or []
            s = str(raw) if raw is not None else ""
            if values:
                matched = best_match(s, [str(v) for v in values])
                try:
                    idx = [str(v) for v in values].index(matched)
                except ValueError:
                    idx = 0
                vec.append(float(idx))
            else:
                m = re.match(r"^(\d+)", s)
                vec.append(float(m.group(1)) if m else 0.0)

        elif kind == "scale":
            if isinstance(raw, (int, float)) and not isinstance(raw, bool):
                vec.append(float(raw))
            else:
                s = str(raw) if raw is not None else ""
                m = re.match(r"^(\d+)", s)
                vec.append(float(m.group(1)) if m else 0.0)
        else:
            vec.append(0.0)

    return np.asarray(vec, dtype=np.float32).reshape(1, -1)


def encode_matrix(
    rows: list[dict[str, Any]],
    plan: list[dict[str, Any]],
    tax: Taxonomy | None = None,
) -> np.ndarray:
    return np.vstack([encode_row(r, plan, tax) for r in rows])


def load_encoder_state(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_encoder_state(state: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
