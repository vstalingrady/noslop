"""Load StoryScope XGBoost weights and score an encoded row."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from xgboost import XGBClassifier


def load_model(path: str | Path) -> XGBClassifier:
    clf = XGBClassifier()
    clf.load_model(str(path))
    return clf


def model_n_features(clf: XGBClassifier) -> int:
    n = getattr(clf, "n_features_in_", None)
    if n is not None:
        return int(n)
    return int(clf.get_booster().num_features())


def predict_binary(clf: XGBClassifier, X: np.ndarray) -> dict[str, Any]:
    """
    Paper binary task: human=1, AI=0.
    Returns P(human), P(AI), label.
    """
    expected = model_n_features(clf)
    if X.shape[1] != expected:
        raise ValueError(
            f"Feature width mismatch: got {X.shape[1]}, model expects {expected}. "
            "Rebuild encoder_state.json against this model."
        )
    proba = clf.predict_proba(X)[0]
    # class order from model
    classes = list(getattr(clf, "classes_", [0, 1]))
    # map
    p_by_class = {int(c): float(p) for c, p in zip(classes, proba)}
    p_human = p_by_class.get(1, 0.0)
    p_ai = p_by_class.get(0, 0.0)
    # if only one class somehow
    if len(p_by_class) == 1:
        only = next(iter(p_by_class))
        if only == 1:
            p_human, p_ai = float(proba[0]), 1.0 - float(proba[0])
        else:
            p_ai, p_human = float(proba[0]), 1.0 - float(proba[0])
    label = "human" if p_human >= p_ai else "AI"
    return {
        "label": label,
        "p_human": p_human,
        "p_ai": p_ai,
        "n_features": int(X.shape[1]),
        "model_n_features": expected,
    }
