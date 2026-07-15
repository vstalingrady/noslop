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
from noslop.template import write_template
from noslop.voice import score_voice


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="noslop",
        description=(
            "noslop: VOICE anti-slop gate + optional StoryScope scorer. "
            "Primary ship path is `voice`; `score` is diagnostic."
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
        help='Feature JSON: {"features": {...}} or flat id→value map',
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
    p_score.add_argument(
        "--min-coverage",
        type=float,
        default=None,
        help="If set, gate FAIL when extracted/expected < this value",
    )
    p_score.add_argument("--json", action="store_true", help="JSON output")
    p_score.add_argument(
        "--dump-features",
        type=Path,
        default=None,
        help="Copy features JSON here",
    )

    p_tpl = sub.add_parser(
        "features-template",
        help="Write empty feature template JSON for agent fill",
    )
    p_tpl.add_argument(
        "--pack",
        choices=["high-gain", "core", "all"],
        default="high-gain",
        help="Which feature pack to include (default high-gain)",
    )
    p_tpl.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output path for template JSON",
    )

    p_voice = sub.add_parser(
        "voice",
        help="Score prose with VOICE anti-slop heuristics (primary gate)",
    )
    p_voice.add_argument(
        "--text-file",
        type=Path,
        required=True,
        help="Path to draft text/markdown",
    )
    p_voice.add_argument(
        "--threshold",
        type=float,
        default=6.5,
        help="PASS if score >= threshold and no hard_fail (default 6.5)",
    )
    p_voice.add_argument("--json", action="store_true", help="JSON output")

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
                min_coverage=args.min_coverage,
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

    if args.cmd == "features-template":
        try:
            path = write_template(args.out, pack=args.pack)
        except Exception as e:
            print(f"features-template failed: {e}", file=sys.stderr)
            return 2
        print(f"wrote {path}")
        return 0

    if args.cmd == "voice":
        if not args.text_file.is_file():
            print(f"Text file not found: {args.text_file}", file=sys.stderr)
            return 2
        text = args.text_file.read_text(encoding="utf-8")
        # strip simple markdown headers for scoring body
        body = "\n".join(
            ln for ln in text.splitlines() if not ln.strip().startswith("#")
        )
        result = score_voice(body, threshold=args.threshold)
        result["path"] = str(args.text_file)
        if args.json:
            print(format_json(result))
        else:
            hf = "yes" if result["hard_fail"] else "no"
            print(
                f"noslop voice\n"
                f"score: {result['score']}\n"
                f"gate: {result['gate'].upper()}  (threshold {result['threshold']})\n"
                f"hard_fail: {hf}\n"
                f"axes: {result['axes']}\n"
                f"ban_hits: {result['details']['ban_hits']}\n"
                f"file: {args.text_file}"
            )
        return 0 if result.get("gate") == "pass" else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
