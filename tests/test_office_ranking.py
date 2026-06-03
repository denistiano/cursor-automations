#!/usr/bin/env python3
"""Tests for office ranking heuristics."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from office_ranking import (  # noqa: E402
    build_rankings,
    is_candidate,
    location_score,
    training_fit_score,
)


class TestOfficeRanking(unittest.TestCase):
    def test_rejects_tiny_office(self) -> None:
        row = {"title": "Офис", "sqm": 20, "priceEur": 200, "location": "Център, Пловдив"}
        self.assertFalse(is_candidate(row))
        row30 = {"title": "Офис", "sqm": 30, "priceEur": 200, "location": "Център, Пловдив"}
        self.assertFalse(is_candidate(row30))

    def test_training_hall_scores_high(self) -> None:
        row = {
            "title": "Зала за обучения и семинари",
            "sqm": 50,
            "priceEur": 400,
            "location": "Център, Пловдив",
            "snippet": "капацитет 22 места",
        }
        self.assertTrue(is_candidate(row))
        self.assertGreater(training_fit_score(row), 0.5)

    def test_kapana_beats_suburb(self) -> None:
        kapana = {"title": "Офис", "location": "Капана, Пловдив", "sqm": 60, "priceEur": 500}
        trakia = {"title": "Офис", "location": "Тракия, Пловдив", "sqm": 60, "priceEur": 500}
        self.assertGreater(location_score(kapana), location_score(trakia))

    def test_build_rankings_returns_four_lists(self) -> None:
        listings = [
            {
                "title": "Зала обучения център",
                "sqm": 55,
                "priceEur": 350,
                "location": "Капана, Пловдив",
                "url": "https://example.com/1",
            },
            {
                "title": "Склад",
                "sqm": 200,
                "priceEur": 100,
                "location": "Коматево",
                "snippet": "склад",
            },
            {
                "title": "Офис представителен",
                "sqm": 90,
                "priceEur": 750,
                "location": "Център, Пловдив",
                "snippet": "луксозен ремонт бизнес център",
                "url": "https://example.com/2",
            },
        ]
        out = build_rankings(listings)
        self.assertIn("top10", out)
        for key in ("luxury", "location", "price", "overall"):
            self.assertIn(key, out["top10"])
            self.assertGreaterEqual(len(out["top10"][key]), 1)


if __name__ == "__main__":
    unittest.main()
