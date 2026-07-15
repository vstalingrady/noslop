"""noslop CLI — local XGBoost score from feature JSON."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from noslop import __version__
from noslop.report import format_json, format_text
from noslop.score import score


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="noslop",
        description=(
            "Local StoryScope XGBoost scorer (arXiv:2604.03136). "
            "Pass --features JSON."
        ),
    )
    parser.add_argument("--version", action="version", version=f"noslop {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_score = sub.add_parser("score", help="Score feature JSON with local XGBoost")
    p_score.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=None,
        help="Label path shown in report (text is not scored)",
    )
    p_score.add_argument(
        "--features",
        type=Path,
        required=True,
        help="Feature JSON: {\"features\": {...}} or flat id→value map",
    )
    p_score.add_argument(
        "--model",
        choices=["narrative", "full"],
        default="narrative",
        help="noslop_binary_narrative (default) or full",
    )
    p_score.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="PASS if P(human) >= threshold (default 0.5)",
    )
    p_score.add_argument("--json", action="store_true", help="JSON output")
    p_score.add_argument(
        "--dump-features",
        type=Path,
        default=None,
        help="Copy features JSON here",
    )

    args = parser.parse_args(argv)

    if args.cmd == "score":
        if not args.features.is_file():
            print(f"Features file not found: {args.features}", file=sys.stderr)
            return 2
        try:
            result = score(
                features_path=args.features,
                model_name=args.model,
                threshold=args.threshold,
                dump_features_path=args.dump_features,
                path_label=str(args.path) if args.path else str(args.features),
            )
        except FileNotFoundError as e:
            print(str(e), file=sys.stderr)
            return 2
        except Exception as e:
            print(f"score failed: {e}", file=sys.stderr)
            return 2

        print(format_json(result) if args.json else format_text(result))
        return 0 if result.get("gate") == "pass" else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
