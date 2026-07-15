"""Load StoryScope taxonomy.json."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Feature:
    id: str
    name: str
    question: str
    type: str
    values: list[str]
    condition: str | None = None
    dimension: str = ""


@dataclass
class Dimension:
    key: str
    name: str
    description: str
    features: list[Feature] = field(default_factory=list)


@dataclass
class Taxonomy:
    dimensions: list[Dimension] = field(default_factory=list)

    @property
    def feature_ids(self) -> list[str]:
        out: list[str] = []
        for dim in self.dimensions:
            for f in dim.features:
                out.append(f.id)
        return out

    @property
    def feature_map(self) -> dict[str, Feature]:
        return {f.id: f for dim in self.dimensions for f in dim.features}

    def narrative_feature_ids(self) -> list[str]:
        """Paper 'narrative' models drop style (STY_*) features."""
        return [fid for fid in self.feature_ids if not fid.startswith("STY_")]

    @classmethod
    def from_json(cls, path: str | Path) -> Taxonomy:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        feature_data = data.get("feature_taxonomy", data)
        tax = cls()
        for dim_key, dim_data in feature_data.items():
            if dim_key in ("taxonomy_metadata", "feature_index"):
                continue
            if not isinstance(dim_data, dict):
                continue
            dim = Dimension(
                key=dim_key,
                name=dim_data.get("dimension_name", dim_key),
                description=dim_data.get("dimension_description", ""),
            )
            for aspect_data in dim_data.get("aspects", {}).values():
                for feat_data in aspect_data.get("features", []):
                    dim.features.append(
                        Feature(
                            id=feat_data["id"],
                            name=feat_data["name"],
                            question=feat_data["question"],
                            type=feat_data["type"],
                            values=[str(v) for v in feat_data.get("values", [])],
                            condition=feat_data.get("condition"),
                            dimension=dim.name,
                        )
                    )
            if dim.features:
                tax.dimensions.append(dim)
        return tax


def normalize_str(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"\s*\([^)]*\)", "", s)
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def best_match(raw_value: str, allowed: list[str]) -> str:
    """StoryScope-style fuzzy match to taxonomy values."""
    if not allowed:
        return raw_value
    raw_norm = normalize_str(raw_value)
    for canonical in allowed:
        if normalize_str(canonical) == raw_norm:
            return canonical
    raw_num = re.match(r"^(\d+)", raw_norm)
    if raw_num:
        num = raw_num.group(1)
        for canonical in allowed:
            c_num = re.match(r"^(\d+)", normalize_str(canonical))
            if c_num and c_num.group(1) == num:
                return canonical
    for canonical in allowed:
        c_norm = normalize_str(canonical)
        if raw_norm.startswith(c_norm) or c_norm.startswith(raw_norm):
            return canonical
    raw_tokens = set(raw_norm.split("_"))
    best_score, best_canonical = 0.0, None
    for canonical in allowed:
        c_tokens = set(normalize_str(canonical).split("_"))
        if not c_tokens:
            continue
        score = len(raw_tokens & c_tokens) / max(len(raw_tokens), len(c_tokens))
        if score > best_score:
            best_score, best_canonical = score, canonical
    if best_score >= 0.33 and best_canonical is not None:
        return best_canonical
    return raw_value


def normalize_features(features: dict[str, Any], tax: Taxonomy) -> dict[str, Any]:
    fmap = tax.feature_map
    out: dict[str, Any] = {}
    for fid, raw_val in features.items():
        if fid not in fmap:
            continue
        f = fmap[fid]
        allowed = list(f.values)
        if raw_val == "n/a" or raw_val is None:
            out[fid] = "n/a"
        elif f.type == "multi_select":
            vals = raw_val if isinstance(raw_val, list) else [raw_val]
            matched = [best_match(str(v), allowed) for v in vals]
            seen: set[str] = set()
            deduped: list[str] = []
            for m in matched:
                key = normalize_str(m)
                if key not in seen:
                    seen.add(key)
                    deduped.append(m)
            out[fid] = deduped
        elif f.type == "scale":
            s = str(raw_val).strip()
            m = re.match(r"^(\d+)", s)
            out[fid] = int(m.group(1)) if m else raw_val
        elif f.type in ("categorical", "ordinal", "binary"):
            out[fid] = best_match(str(raw_val), allowed)
        else:
            out[fid] = raw_val
    return out
