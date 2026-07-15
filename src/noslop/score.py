"""Local StoryScope XGBoost score from feature JSON only."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from noslop.encode import encode_row, load_encoder_state
from noslop.extract import load_features_json
from noslop.paths import (
    ENCODER_STATE_PATH,
    MODEL_FILES,
    TAXONOMY_PATH,
    require_file,
)
from noslop.predict import load_model, predict_binary
from noslop.taxonomy import Taxonomy


def score(
    *,
    features: dict[str, Any] | None = None,
    features_path: str | Path | None = None,
    model_name: str = "narrative",
    threshold: float = 0.5,
    dump_features_path: str | Path | None = None,
    path_label: str | None = None,
) -> dict[str, Any]:
    """
    Score with local XGBoost. Requires features (dict or JSON path).
    No LLM / API extraction.
    """
    tax = Taxonomy.from_json(require_file(TAXONOMY_PATH))
    enc = load_encoder_state(
        require_file(ENCODER_STATE_PATH, "Run: python -m noslop.tools.build_encoder")
    )

    if model_name not in ("narrative", "full"):
        raise ValueError("model_name must be 'narrative' or 'full'")
    plan = enc["plans"][model_name]
    feature_ids = enc["feature_ids"][model_name]

    if features is None and features_path is not None:
        features = load_features_json(features_path)
    if features is None:
        raise ValueError(
            "features or features_path required. "
            "No live API extract — fill features in-session or pass --features JSON."
        )

    if dump_features_path:
        import json

        Path(dump_features_path).write_text(
            json.dumps({"features": features}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    X = encode_row(features, plan, tax)
    model_path = require_file(
        MODEL_FILES[model_name],
        "Train: python -m noslop.tools.train_binary --subset narrative",
    )
    clf = load_model(model_path)
    pred = predict_binary(clf, X)

    p_human = pred["p_human"]
    gate = "pass" if p_human >= threshold else "fail"
    extracted = sum(
        1 for fid in feature_ids if fid in features and features[fid] not in (None, "")
    )

    return {
        **pred,
        "gate": gate,
        "threshold": threshold,
        "model_name": f"binary_{model_name}",
        "model_path": str(model_path),
        "features_extracted": extracted,
        "features_expected": len(feature_ids),
        "extractor_model": None,
        "warning": None,
        "paper": "arXiv:2604.03136",
        "path": path_label or (str(features_path) if features_path else None),
    }
