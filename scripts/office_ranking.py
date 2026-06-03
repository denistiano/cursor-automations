#!/usr/bin/env python3
"""Score and rank Plovdiv office listings for Vibe Coders Academy (training ~20 students)."""

from __future__ import annotations

import re
from typing import Any

SOFT_BUDGET_EUR = 800
MIN_SQM = 40
TARGET_SQM = 80
TOP_N = 10

CENTRAL_AREAS: list[tuple[str, float]] = [
    (r"капана|kapana", 1.0),
    (r"център|tsentar|center", 0.95),
    (r"главн|main\s*street", 0.9),
    (r"стар(ият)?\s*град|old\s*town", 0.88),
    (r"дондуков|dondoukov", 0.85),
    (r"иван\s*вазов|ivan\s*vazov", 0.82),
    (r"университет|university", 0.8),
    (r"съединение|saedinenie", 0.78),
    (r"джумая|dzhumaya", 0.78),
    (r"римски\s*стадион", 0.75),
    (r"кършияка|karshiyaka", 0.55),
    (r"тракия|trakia", 0.35),
    (r"коматево|komatevo", 0.3),
    (r"смирненски|smirnenski", 0.45),
    (r"пролом|prolom", 0.7),
    (r"хан\s*кубрат", 0.85),
    (r"делови\s*център|business\s*center", 0.8),
]

LUXURY_HINTS: list[tuple[str, float]] = [
    (r"лукс|luxury|представител", 0.35),
    (r"ремонтиран|renovat|нов\s*ремонт", 0.25),
    (r"модерн|elegant|елегант", 0.2),
    (r"бизнес\s*център|business\s*center|делови\s*център", 0.25),
    (r"клас\s*[аa]|class\s*a", 0.2),
    (r"паркинг|parking|гараж", 0.1),
    (r"климатик|air\s*condition|hvac", 0.08),
    (r"executive|премиум|premium|vip", 0.2),
]

TRAINING_HINTS: list[tuple[str, float]] = [
    (r"обучен|training|курс|course", 0.35),
    (r"семинар|seminar|лекци|lecture", 0.3),
    (r"зала|hall|classroom|класна", 0.35),
    (r"уъркшоп|workshop|презентац", 0.25),
    (r"капацитет|места|seats|students", 0.2),
    (r"школа|school|академ", 0.15),
]

EXCLUDE_RE = re.compile(
    r"фризьор|маникюр|салон за красота|бърза закуска|палачинк|бургер|пица|склад|storage|"
    r"търговско\s*помещение|хале|складов",
    re.I,
)

SHOP_ONLY_RE = re.compile(r"^магазин\b|магазин\s+\d+\s*кв", re.I)


def listing_blob(row: dict) -> str:
    return " ".join(
        str(row.get(k) or "")
        for k in ("title", "location", "snippet", "url")
    ).lower()


def location_score(row: dict) -> float:
    blob = listing_blob(row)
    best = 0.35
    for pat, weight in CENTRAL_AREAS:
        if re.search(pat, blob, re.I):
            best = max(best, weight)
    return best


def luxury_score(row: dict) -> float:
    blob = listing_blob(row)
    score = 0.0
    price = row.get("priceEur")
    sqm = row.get("sqm")
    if price and sqm and sqm > 0:
        per_sqm = price / sqm
        if per_sqm >= 12:
            score += 0.35
        elif per_sqm >= 8:
            score += 0.22
        elif per_sqm >= 5:
            score += 0.1
    if price:
        if price >= 700:
            score += 0.25
        elif price >= 500:
            score += 0.15
        elif price >= 350:
            score += 0.08
    for pat, weight in LUXURY_HINTS:
        if re.search(pat, blob, re.I):
            score += weight
    if sqm and sqm >= 100:
        score += 0.15
    elif sqm and sqm >= 70:
        score += 0.08
    return min(score, 1.0)


def training_fit_score(row: dict) -> float:
    blob = listing_blob(row)
    if EXCLUDE_RE.search(blob) and not re.search(r"зала|обучен|офис", blob, re.I):
        return 0.0
    if SHOP_ONLY_RE.search(row.get("title") or "") and not re.search(
        r"зала|обучен|семинар|офис", blob, re.I
    ):
        return 0.0
    score = 0.25
    sqm = row.get("sqm")
    if sqm is not None:
        if sqm < MIN_SQM:
            return 0.0
        if sqm > 280 and not re.search(r"зала|обучен|семинар|клас", blob, re.I):
            return 0.0
        if sqm >= TARGET_SQM:
            score += 0.45
        elif sqm >= 55:
            score += 0.35
        elif sqm >= MIN_SQM:
            score += 0.2
    else:
        score += 0.1
    for pat, weight in TRAINING_HINTS:
        if re.search(pat, blob, re.I):
            score += weight
    cap = re.search(r"(\d{1,2})\s*(?:места|seats|учащ|студент)", blob, re.I)
    if cap:
        n = int(cap.group(1))
        if n >= 18:
            score += 0.25
        elif n >= 12:
            score += 0.12
    return min(score, 1.0)


def price_value_score(row: dict) -> float:
    price = row.get("priceEur")
    sqm = row.get("sqm")
    if training_fit_score(row) <= 0:
        return 0.0
    if not price or price <= 0:
        return 0.15
    if price > SOFT_BUDGET_EUR * 1.5:
        return max(0.05, 0.4 - (price - SOFT_BUDGET_EUR) / 2000)
    base = 1.0 - (price / (SOFT_BUDGET_EUR * 1.25))
    if sqm and sqm >= MIN_SQM:
        usable = min(sqm, TARGET_SQM * 1.5)
        base += min(0.35, (usable / TARGET_SQM) * 0.2)
    return max(0.0, min(base, 1.0))


def overall_score(row: dict) -> float:
    loc = location_score(row)
    lux = luxury_score(row)
    fit = training_fit_score(row)
    price = price_value_score(row)
    if fit <= 0:
        return 0.0
    score = fit * 0.35 + loc * 0.3 + lux * 0.15 + price * 0.2
    rent = row.get("priceEur")
    if rent and rent > SOFT_BUDGET_EUR:
        over = min(1.0, (rent - SOFT_BUDGET_EUR) / SOFT_BUDGET_EUR)
        score *= max(0.35, 1.0 - over * 0.55)
    return score


def is_candidate(row: dict) -> bool:
    if training_fit_score(row) <= 0:
        return False
    sqm = row.get("sqm")
    if sqm is not None and sqm < MIN_SQM:
        return False
    return True


def enrich_listing(row: dict) -> dict:
    out = dict(row)
    out["scores"] = {
        "location": round(location_score(row), 3),
        "luxury": round(luxury_score(row), 3),
        "trainingFit": round(training_fit_score(row), 3),
        "priceValue": round(price_value_score(row), 3),
        "overall": round(overall_score(row), 3),
    }
    price = row.get("priceEur")
    out["withinSoftBudget"] = price is None or price <= SOFT_BUDGET_EUR
    return out


def top_n(listings: list[dict], key: str, n: int = TOP_N) -> list[dict]:
    candidates = [enrich_listing(r) for r in listings if is_candidate(r)]
    ranked = sorted(candidates, key=lambda r: r["scores"][key], reverse=True)
    result: list[dict] = []
    for i, row in enumerate(ranked[:n], start=1):
        item = dict(row)
        item["rank"] = i
        result.append(item)
    return result


def build_rankings(listings: list[dict]) -> dict[str, Any]:
    enriched = [enrich_listing(r) for r in listings if is_candidate(r)]
    return {
        "criteria": {
            "minSqm": MIN_SQM,
            "targetSqm": TARGET_SQM,
            "softBudgetEur": SOFT_BUDGET_EUR,
            "use": "Training space for ~20 students (classroom / hall)",
            "candidateCount": len(enriched),
        },
        "top10": {
            "luxury": top_n(listings, "luxury"),
            "location": top_n(listings, "location"),
            "price": top_n(listings, "priceValue"),
            "overall": top_n(listings, "overall"),
        },
    }
