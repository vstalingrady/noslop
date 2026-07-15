"""
Build encoder_state.json from StoryScope taxonomy (no parquet required).

  python -m noslop.tools.build_encoder
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from noslop.encode import build_column_plan, save_encoder_state
from noslop.paths import ENCODER_STATE_PATH, TAXONOMY_PATH
from noslop.taxonomy import Taxonomy


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--taxonomy", type=Path, default=TAXONOMY_PATH)
    p.add_argument("--out", type=Path, default=ENCODER_STATE_PATH)
    args = p.parse_args(argv)

    tax = Taxonomy.from_json(args.taxonomy)
    full_ids = tax.feature_ids
    narr_ids = tax.narrative_feature_ids()
    plans = {
        "full": build_column_plan(tax, full_ids),
        "narrative": build_column_plan(tax, narr_ids),
    }
    state = {
        "version": 2,
        "encoding": "paper-style: cat one-hot, multi multi-hot, ordinal index, scale numeric, binary 0/1",
        "paper": "arXiv:2604.03136",
        "note": (
            "Column layout is taxonomy-derived. Trained weights in "
            "artifacts/models/noslop_binary_*.json match this layout. "
            "Upstream StoryScope binary_*.json use a different unpublished layout."
        ),
        "feature_ids": {"full": full_ids, "narrative": narr_ids},
        "plans": {
            k: [
                {kk: vv for kk, vv in col.items() if kk != "values" or True}
                for col in plan
            ]
            for k, plan in plans.items()
        },
        "n_columns": {k: len(v) for k, v in plans.items()},
    }
    # plans are JSON-serializable
    save_encoder_state(state, args.out)
    print(f"wrote {args.out}")
    print(f"columns narrative={len(plans['narrative'])} full={len(plans['full'])}")
    print(f"features narrative={len(narr_ids)} full={len(full_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
