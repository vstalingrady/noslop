"""
Train binary human-vs-AI XGBoost on StoryScope feature parquet.

Uses paper hyperparameters (binary): n_estimators=420, max_depth=8, reg_lambda=2,
human sample weight 5. Same 304 features / taxonomy as StoryScope.

  # place storyscope_features.parquet under artifacts/ (or pass --features)
  pip install pyarrow
  python -m noslop.tools.train_binary
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from noslop.encode import build_column_plan, encode_row, load_encoder_state
from noslop.paths import (
    ENCODER_STATE_PATH,
    FEATURES_PARQUET,
    MODELS_DIR,
    TAXONOMY_PATH,
)
from noslop.taxonomy import Taxonomy


def _load_rows(path: Path) -> list[dict]:
    try:
        import pyarrow.parquet as pq
    except ImportError as e:
        raise SystemExit("pip install pyarrow") from e
    return pq.read_table(path).to_pylist()


def main(argv: list[str] | None = None) -> int:
    from xgboost import XGBClassifier

    p = argparse.ArgumentParser()
    p.add_argument(
        "--features",
        type=Path,
        default=FEATURES_PARQUET,
        help="StoryScope storyscope_features.parquet (default: artifacts/)",
    )
    p.add_argument("--taxonomy", type=Path, default=TAXONOMY_PATH)
    p.add_argument("--encoder", type=Path, default=ENCODER_STATE_PATH)
    p.add_argument(
        "--subset",
        choices=["narrative", "full"],
        default="narrative",
        help="narrative = drop STY_* (default, paper headline)",
    )
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--limit", type=int, default=None, help="debug: limit rows")
    args = p.parse_args(argv)

    if not args.encoder.is_file():
        print("Building encoder_state first...")
        from noslop.tools.build_encoder import main as build_main

        build_main([])

    enc = load_encoder_state(args.encoder)
    tax = Taxonomy.from_json(args.taxonomy)
    plan = enc["plans"][args.subset]
    feature_ids = enc["feature_ids"][args.subset]
    # rebuild plan objects if stored without kinds intact
    if plan and "kind" not in plan[0]:
        plan = build_column_plan(tax, feature_ids)

    rows = _load_rows(args.features)
    if args.limit:
        # stratified sample by source so we don't get all-human prefix slices
        by_src: dict[str, list] = {}
        for r in rows:
            src = str(r.get("source") or r.get("author") or "unk")
            by_src.setdefault(src, []).append(r)
        rng = np.random.RandomState(42)
        per = max(1, args.limit // max(1, len(by_src)))
        sampled: list = []
        for src, lst in by_src.items():
            idx = rng.choice(len(lst), size=min(per, len(lst)), replace=False)
            sampled.extend(lst[i] for i in idx)
        rng.shuffle(sampled)
        rows = sampled[: args.limit]
    print(f"rows={len(rows)} cols={len(plan)} subset={args.subset}")

    X_list = []
    y_list = []
    groups = []
    for r in rows:
        source = str(r.get("source") or r.get("author") or "")
        feats = {fid: r.get(fid) for fid in feature_ids}
        X_list.append(encode_row(feats, plan, tax)[0])
        y_list.append(1 if source == "human" else 0)
        groups.append(r.get("prompt_id", r.get("story_title")))

    X = np.asarray(X_list, dtype=np.float32)
    y = np.asarray(y_list, dtype=np.int32)
    print(f"X={X.shape} human={y.sum()} ai={(y == 0).sum()}")

    # prompt-level holdout ~20%
    uniq = sorted(set(groups))
    rng = np.random.RandomState(42)
    rng.shuffle(uniq)
    n_test = max(1, int(0.2 * len(uniq)))
    test_g = set(uniq[:n_test])
    train_mask = np.array([g not in test_g for g in groups])
    test_mask = ~train_mask

    sample_weight = np.where(y[train_mask] == 1, 5.0, 1.0)
    clf = XGBClassifier(
        n_estimators=420,
        max_depth=8,
        reg_lambda=2.0,
        eval_metric="logloss",
        random_state=42,
    )
    clf.fit(X[train_mask], y[train_mask], sample_weight=sample_weight)

    pred = clf.predict(X[test_mask])
    acc = float((pred == y[test_mask]).mean())
    # macro-F1 rough
    def f1(label: int) -> float:
        tp = int(((pred == label) & (y[test_mask] == label)).sum())
        fp = int(((pred == label) & (y[test_mask] != label)).sum())
        fn = int(((pred != label) & (y[test_mask] == label)).sum())
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        return 2 * prec * rec / (prec + rec) if prec + rec else 0.0

    macro = (f1(0) + f1(1)) / 2
    print(f"holdout acc={acc:.4f} macroF1={macro:.4f}")

    out = args.out or (MODELS_DIR / f"noslop_binary_{args.subset}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    clf.save_model(str(out))
    meta = {
        "subset": args.subset,
        "n_features": int(X.shape[1]),
        "n_train": int(train_mask.sum()),
        "n_test": int(test_mask.sum()),
        "holdout_acc": acc,
        "holdout_macro_f1": macro,
        "hyperparameters": {
            "n_estimators": 420,
            "max_depth": 8,
            "reg_lambda": 2.0,
            "human_weight": 5.0,
        },
        "paper": "arXiv:2604.03136",
        "encoding": enc.get("encoding"),
    }
    out.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"saved {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
