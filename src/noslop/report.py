"""Format score reports."""

from __future__ import annotations

import json
from typing import Any


def format_text(result: dict[str, Any]) -> str:
    gate = "PASS" if result.get("gate") == "pass" else "FAIL"
    lines = [
        f"noslop (StoryScope {result.get('model_name', 'binary')})",
        f"label: {result.get('label')}",
        f"P(human): {result.get('p_human', 0):.4f}",
        f"P(AI): {result.get('p_ai', 0):.4f}",
        f"features: {result.get('features_extracted', '?')}/{result.get('features_expected', '?')}",
        f"gate: {gate}  (threshold P(human)>={result.get('threshold', 0.5)})",
    ]
    if result.get("extractor_model"):
        lines.append(f"extractor: {result['extractor_model']}")
    if result.get("warning"):
        lines.append(f"warning: {result['warning']}")
    if result.get("path"):
        lines.append(f"file: {result['path']}")
    return "\n".join(lines)


def format_json(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2)
