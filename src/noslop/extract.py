"""
Feature extraction via StoryScope stage-5 logic.

Default: import extract helpers from the vendored StoryScope package when
available. Fallback: local reimplementation of the same prompt shape.

LLM client is optional — only needed for live extract. Prefer:
  pip install openai
  set OPENAI_API_KEY
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from noslop.paths import STORYSCOPE_ROOT
from noslop.taxonomy import Dimension, Taxonomy, normalize_features


def _ensure_storyscope_on_path() -> None:
    root = str(STORYSCOPE_ROOT)
    if root not in sys.path and (STORYSCOPE_ROOT / "storyscope").is_dir():
        sys.path.insert(0, root)


def build_dimension_prompt(dimension: Dimension, story_text: str) -> str:
    """Same structure as StoryScope apply_features.build_dimension_prompt."""
    feature_specs: list[str] = []
    for f in dimension.features:
        values_str = ", ".join(str(v) for v in f.values[:10])
        if len(f.values) > 10:
            values_str += f" (+ {len(f.values) - 10} more)"
        feature_specs.append(f"**{f.id}** [{f.type}]: {f.question}")
        feature_specs.append(f"  → Values: {values_str}")
        if f.condition:
            feature_specs.append(f"  → Condition: {f.condition}")
    features_block = "\n".join(feature_specs)
    max_chars = 280000
    if len(story_text) > max_chars:
        story_text = story_text[:max_chars] + "\n\n[... story truncated ...]"
    return f"""You are a literary analyst specializing in {dimension.name.lower()}.

Extract structured features about **{dimension.name}** from the story below.
Focus area: {dimension.description}

# FEATURES TO EXTRACT

For each feature, select the appropriate value(s) from the allowed options.

**Response format rules:**
- For "binary" features: respond with exactly "yes" or "no"
- For "categorical" features: respond with exactly ONE value from the list
- For "ordinal" features: respond with exactly ONE value from the list
- For "multi_select" features: respond with a JSON array of ALL applicable values
- For "scale" features: respond with an integer within the specified range
- ONLY use values from the provided lists
- If a feature has a condition that is not met, use "n/a"
- **Never use null or omit a key** — every feature must have a value

{features_block}

# STORY TO ANALYZE

<story>
{story_text}
</story>

# OUTPUT

Return a single JSON object with feature IDs as keys.
"""


def _openai_json(prompt: str, model: str) -> dict[str, Any]:
    """Minimal OpenAI Chat Completions JSON call (stdlib urllib only)."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set (needed for feature extraction)")
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Respond with valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI HTTP {e.code}: {err}") from e
    content = payload["choices"][0]["message"]["content"]
    return json.loads(content)


def extract_features(
    text: str,
    tax: Taxonomy,
    *,
    model: str | None = None,
    dim_workers: int = 5,
) -> tuple[dict[str, Any], str]:
    """
    Extract all taxonomy features for one document.
    Returns (normalized_features, extractor_model_id).
    """
    model = model or os.environ.get("NOSLOP_EXTRACT_MODEL", "gpt-4o-mini")
    all_features: dict[str, Any] = {}

    def one(dim: Dimension) -> tuple[str, dict[str, Any]]:
        prompt = build_dimension_prompt(dim, text)
        result = _openai_json(prompt, model)
        clean = {k: v for k, v in result.items() if not str(k).startswith("_")}
        return dim.key, clean

    with ThreadPoolExecutor(max_workers=dim_workers) as ex:
        futs = {ex.submit(one, dim): dim for dim in tax.dimensions}
        for fut in as_completed(futs):
            dim = futs[fut]
            try:
                _, feats = fut.result()
                all_features.update(feats)
            except Exception as e:
                raise RuntimeError(f"Dimension {dim.key} failed: {e}") from e

    return normalize_features(all_features, tax), model


def load_features_json(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if "features" in data and isinstance(data["features"], dict):
        return data["features"]
    return data
