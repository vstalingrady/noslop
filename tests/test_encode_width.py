"""Offline tests: encoder width vs released StoryScope models."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from noslop.encode import encode_row, load_encoder_state
from noslop.paths import ENCODER_STATE_PATH, MODEL_FILES, TAXONOMY_PATH
from noslop.predict import load_model, model_n_features, predict_binary
from noslop.taxonomy import Taxonomy


class TestEncoder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not ENCODER_STATE_PATH.is_file():
            raise unittest.SkipTest(
                f"missing {ENCODER_STATE_PATH}; run python -m noslop.tools.build_encoder"
            )
        cls.state = load_encoder_state(ENCODER_STATE_PATH)
        cls.tax = Taxonomy.from_json(TAXONOMY_PATH)

    def test_narrative_width_matches_model(self):
        plan = self.state["plans"]["narrative"]
        model_path = MODEL_FILES["narrative"]
        if not model_path.is_file():
            self.skipTest(f"missing {model_path}; run train_binary")
        clf = load_model(model_path)
        self.assertEqual(len(plan), model_n_features(clf))

    def test_encode_and_predict_runs(self):
        plan = self.state["plans"]["narrative"]
        model_path = MODEL_FILES["narrative"]
        if not model_path.is_file():
            self.skipTest(f"missing {model_path}")
        feats = {}
        X = encode_row(feats, plan, self.tax)
        clf = load_model(model_path)
        out = predict_binary(clf, X)
        self.assertIn(out["label"], ("human", "AI"))
        self.assertAlmostEqual(out["p_human"] + out["p_ai"], 1.0, places=5)

    def test_encoder_column_counts(self):
        self.assertEqual(self.state["n_columns"]["narrative"], len(self.state["plans"]["narrative"]))
        self.assertEqual(self.state["n_columns"]["full"], len(self.state["plans"]["full"]))
        self.assertGreater(self.state["n_columns"]["narrative"], 100)


if __name__ == "__main__":
    unittest.main()
