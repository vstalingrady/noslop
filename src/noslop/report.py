"""Format score reports."""

from __future__ import annotations

import json
from typing import Any


def format_text(result: dict[str, Any]) -> str:
    gate = "PASS" if result.get("gate") == "pass" else "FAIL"
    cov = result.get("coverage")
    cov_s = f"{cov:.4f}" if isinstance(cov, (int, float)) else "?"
    lines = [
        f"noslop (StoryScope {result.get('model_name', 'binary')})",
        f"label: {result.get('label')}",
        f"P(human): {result.get('p_human', 0):.4f}",
        f"P(AI): {result.get('p_ai', 0):.4f}",
        f"features: {result.get('features_extracted', '?')}/{result.get('features_expected', '?')}",
        f"coverage: {cov_s}",
        f"gate: {gate}  (threshold P(human)>={result.get('threshold', 0.5)})",
    ]
    if result.get("min_coverage") is not None:
        lines.append(f"min_coverage: {result['min_coverage']}")
    if result.get("extractor_model"):
        lines.append(f"extractor: {result['extractor_model']}")
    if result.get("warning"):
        lines.append(f"warning: {result['warning']}")
    if result.get("path"):
        lines.append(f"file: {result['path']}")
    return "\n".join(lines)


def format_json(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2)
