"""Resolve repo / artifact paths."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = REPO_ROOT / "artifacts"
MODELS_DIR = ARTIFACTS / "models"
TAXONOMY_PATH = ARTIFACTS / "taxonomy.json"
ENCODER_STATE_PATH = ARTIFACTS / "encoder_state.json"
# Optional local copy of StoryScope feature parquet for retrain
FEATURES_PARQUET = ARTIFACTS / "storyscope_features.parquet"

MODEL_FILES = {
    "narrative": MODELS_DIR / "noslop_binary_narrative.json",
    "full": MODELS_DIR / "noslop_binary_full.json",
}


def require_file(path: Path, hint: str = "") -> Path:
    if not path.is_file():
        msg = f"Missing required file: {path}"
        if hint:
            msg += f"\n{hint}"
        raise FileNotFoundError(msg)
    return path
