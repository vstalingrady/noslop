"""End-to-end StoryScope score for one text or feature JSON."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from noslop.encode import encode_row, load_encoder_state
from noslop.extract import extract_features, load_features_json
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
    text: str | None = None,
    features: dict[str, Any] | None = None,
    features_path: str | Path | None = None,
    text_path: str | Path | None = None,
    model_name: str = "narrative",
    threshold: float = 0.5,
    extract_model: str | None = None,
    dump_features_path: str | Path | None = None,
) -> dict[str, Any]:
    """
    Score with StoryScope binary XGBoost.

    Provide one of: text, text_path, features, features_path.
    model_name: 'narrative' (default, paper headline) or 'full'.
    """
    tax = Taxonomy.from_json(require_file(TAXONOMY_PATH))
    enc = load_encoder_state(require_file(ENCODER_STATE_PATH, "Run: python -m noslop.tools.build_encoder"))

    if model_name not in ("narrative", "full"):
        raise ValueError("model_name must be 'narrative' or 'full'")
    plan = enc["plans"][model_name]
    feature_ids = enc["feature_ids"][model_name]

    extractor_model = None
    warning = None

    if features is None and features_path is not None:
        features = load_features_json(features_path)
    if features is None:
        if text is None and text_path is not None:
            text = Path(text_path).read_text(encoding="utf-8")
        if text is None:
            raise ValueError("Need text, text_path, features, or features_path")
        word_count = len(text.split())
        if word_count < 200:
            warning = (
                f"text is short ({word_count} words); StoryScope trained on ~5k-word fiction"
            )
        features, extractor_model = extract_features(
            text, tax, model=extract_model
        )

    if dump_features_path:
        import json

        Path(dump_features_path).write_text(
            json.dumps({"features": features}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    X = encode_row(features, plan, tax)
    model_path = require_file(MODEL_FILES[model_name])
    clf = load_model(model_path)
    pred = predict_binary(clf, X)

    p_human = pred["p_human"]
    gate = "pass" if p_human >= threshold else "fail"
    extracted = sum(1 for fid in feature_ids if fid in features and features[fid] not in (None, ""))

    return {
        **pred,
        "gate": gate,
        "threshold": threshold,
        "model_name": f"binary_{model_name}",
        "model_path": str(model_path),
        "features_extracted": extracted,
        "features_expected": len(feature_ids),
        "extractor_model": extractor_model,
        "warning": warning,
        "paper": "arXiv:2604.03136",
        "path": str(text_path) if text_path else None,
    }
