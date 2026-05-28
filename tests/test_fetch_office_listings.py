#!/usr/bin/env python3
"""Tests for office listing parsers (no network)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from fetch_office_listings import (  # noqa: E402
    fits_criteria,
    merge_listings,
    parse_alo_page,
    parse_eur,
    parse_imot_page,
    parse_sqm,
)

ALO_FIXTURE = """
<div id="adrows_11111111" title="Офис под наем център">
  <a href="/ofis-test-11111111"></a>
  <div class="listvip-item-title">Офис под наем - тест</div>
  <span>Месечен наем : 420 €</span>
  <span>37 кв.м</span>
  <div class="listvip-item-address">Център, Пловдив</div>
</div>
<div id="adrows_22222222" title="Салон">
  <a href="/salon-za-krasota-pod-naem-22222222"></a>
  <div class="listvip-item-title">Салон за красота</div>
  <span>200 €</span>
  <span>30 кв.м</span>
  <div class="listvip-item-address">Център, Пловдив</div>
</div>
"""

IMOT_FIXTURE = """
<a href="//www.imot.bg/obiava-2h100-dava-pod-naem-ofis-grad-plovdiv-tsentar">
  Дава под наем ОФИС 500 € 978.00 лв. 45 кв.м, Център
</a>
<a href="//www.imot.bg/obiava-2h200-dava-pod-naem-ofis-grad-plovdiv-karshiyaka">
  Дава под наем ОФИС 1200 € 2 346.00 лв. 80 кв.м
</a>
"""


class TestOfficeParsers(unittest.TestCase):
    def test_parse_eur_and_sqm(self) -> None:
        self.assertEqual(parse_eur("Месечен наем : 420 € (821 лв.)"), 420.0)
        self.assertEqual(parse_sqm("площ 37 кв.м"), 37.0)

    def test_parse_alo_page_filters_salon(self) -> None:
        rows = parse_alo_page(ALO_FIXTURE)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["priceEur"], 420.0)
        self.assertIn("alo.bg", rows[0]["url"])

    def test_parse_imot_page(self) -> None:
        rows = parse_imot_page(IMOT_FIXTURE)
        self.assertEqual(len(rows), 2)
        prices = sorted(r["priceEur"] for r in rows if r["priceEur"])
        self.assertEqual(prices, [500.0, 1200.0])

    def test_fits_criteria_budget(self) -> None:
        self.assertTrue(fits_criteria({"priceEur": 500}, 800))
        self.assertTrue(fits_criteria({"priceEur": None}, 800))
        self.assertFalse(fits_criteria({"priceEur": 1200}, 800))

    def test_merge_prefers_url(self) -> None:
        merged = merge_listings(
            [{"title": "A", "priceEur": 400, "url": "", "source": "alo.bg"}],
            [{"title": "A longer", "priceEur": 400, "url": "https://www.alo.bg/x", "source": "alo.bg"}],
        )
        self.assertEqual(len(merged), 1)
        self.assertTrue(merged[0]["url"])


if __name__ == "__main__":
    unittest.main()
