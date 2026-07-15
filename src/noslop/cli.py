"""noslop CLI — score text with StoryScope paper models."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# editable / repo run
_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from noslop import __version__
from noslop.report import format_json, format_text
from noslop.score import score


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="noslop",
        description="Score writing with StoryScope (arXiv:2604.03136) XGBoost detectors",
    )
    parser.add_argument("--version", action="version", version=f"noslop {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_score = sub.add_parser("score", help="Score a text file (StoryScope human vs AI)")
    p_score.add_argument("path", type=Path, help="Text file to score")
    p_score.add_argument(
        "--model",
        choices=["narrative", "full"],
        default="narrative",
        help="binary_narrative (default) or binary_full",
    )
    p_score.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="PASS if P(human) >= threshold (default 0.5)",
    )
    p_score.add_argument("--json", action="store_true", help="JSON output")
    p_score.add_argument(
        "--features",
        type=Path,
        default=None,
        help="Skip LLM extract; use precomputed features JSON",
    )
    p_score.add_argument(
        "--dump-features",
        type=Path,
        default=None,
        help="Write extracted features JSON here",
    )
    p_score.add_argument(
        "--extract-model",
        default=None,
        help="OpenAI model for feature extraction (default gpt-4o-mini / NOSLOP_EXTRACT_MODEL)",
    )

    args = parser.parse_args(argv)

    if args.cmd == "score":
        if not args.path.is_file() and args.features is None:
            print(f"File not found: {args.path}", file=sys.stderr)
            return 2
        try:
            if args.features is not None:
                result = score(
                    features_path=args.features,
                    model_name=args.model,
                    threshold=args.threshold,
                    dump_features_path=args.dump_features,
                )
                result["path"] = str(args.path) if args.path else str(args.features)
            else:
                result = score(
                    text_path=args.path,
                    model_name=args.model,
                    threshold=args.threshold,
                    extract_model=args.extract_model,
                    dump_features_path=args.dump_features,
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
