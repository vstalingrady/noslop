"""Resolve repo / artifact paths."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = REPO_ROOT / "artifacts"
MODELS_DIR = ARTIFACTS / "models"
TAXONOMY_PATH = ARTIFACTS / "taxonomy.json"
ENCODER_STATE_PATH = ARTIFACTS / "encoder_state.json"
STORYSCOPE_ROOT = REPO_ROOT / "third_party" / "storyscope"
DEFAULT_CONFIG = REPO_ROOT / "config" / "models.yaml"

# Prefer noslop-trained weights (match encoder_state). Upstream StoryScope
# binary_*.json kept for reference but need different column layout.
MODEL_FILES = {
    "narrative": MODELS_DIR / "noslop_binary_narrative.json",
    "full": MODELS_DIR / "noslop_binary_full.json",
}

UPSTREAM_MODEL_FILES = {
    "narrative": MODELS_DIR / "binary_narrative.json",
    "full": MODELS_DIR / "binary_full.json",
}


def require_file(path: Path, hint: str = "") -> Path:
    if not path.is_file():
        msg = f"Missing required file: {path}"
        if hint:
            msg += f"\n{hint}"
        raise FileNotFoundError(msg)
    return path
