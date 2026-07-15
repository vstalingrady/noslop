"""Load precomputed feature JSON. No network / no API extract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_features_json(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if "features" in data and isinstance(data["features"], dict):
        return data["features"]
    if not isinstance(data, dict):
        raise ValueError(f"features file must be a JSON object: {path}")
    return data
