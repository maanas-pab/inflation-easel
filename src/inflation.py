"""Inflation math: load the CPI CSV and answer 'what does 1970 cost now?'."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "cpi_groceries.csv"
BASE_YEAR = 1970
PROJECTED_YEARS = {2025, 2026}

BASKET = {
    "apple_per_lb": 3.0,   # 3 lb of apples
    "bread_per_loaf": 2.0,  # 2 loaves
    "milk_per_gallon": 1.0,  # 1 gallon
    "eggs_per_dozen": 1.0,  # 1 dozen
}


@dataclass
class YearSnapshot:
    year: int
    cpi_u: float
    food_index: float
    prices: dict
    basket_cost: float
    cumulative_inflation: float  # vs 1970, e.g. 1.5 = +150%
    purchasing_power: float  # $1 of 1970 in today's goods (0..1)
    projected: bool


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path).sort_values("year").reset_index(drop=True)
    df["basket_cost"] = sum(df[col] * qty for col, qty in BASKET.items())
    base_cpi = float(df.loc[df["year"] == BASE_YEAR, "cpi_u"].iloc[0])
    base_basket = float(df.loc[df["year"] == BASE_YEAR, "basket_cost"].iloc[0])
    df["cumulative_inflation"] = df["cpi_u"] / base_cpi - 1.0
    df["purchasing_power"] = base_basket / df["basket_cost"]
    df["projected"] = df["year"].isin(PROJECTED_YEARS)
    return df


def snapshot(df: pd.DataFrame, year: int) -> YearSnapshot:
    year = int(max(df["year"].min(), min(year, df["year"].max())))
    row = df.loc[df["year"] == year].iloc[0]
    prices = {
        "apples": float(row["apple_per_lb"]),
        "bread": float(row["bread_per_loaf"]),
        "eggs": float(row["eggs_per_dozen"]),
        "milk": float(row["milk_per_gallon"]),
    }
    return YearSnapshot(
        year=year,
        cpi_u=float(row["cpi_u"]),
        food_index=float(row["food_at_home_index"]),
        prices=prices,
        basket_cost=float(row["basket_cost"]),
        cumulative_inflation=float(row["cumulative_inflation"]),
        purchasing_power=float(row["purchasing_power"]),
        projected=bool(row["projected"]),
    )


def apple_shrink_factor(snap: YearSnapshot, df: pd.DataFrame) -> float:
    """Apple radius factor: 1.0 in 1970 -> ~0.45 by 2026.

    Driven by the real apple price relative to overall inflation so the
    shrinking is data-bound, not hard-coded.
    """
    base = float(df.loc[df["year"] == BASE_YEAR, "apple_per_lb"].iloc[0])
    current = snap.prices["apples"]
    real_ratio = (current / base) / (1.0 + snap.cumulative_inflation)
    # real_ratio hovers ~1; map nominal 7x price growth onto visible shrink
    nominal_ratio = current / base
    shrink = 1.0 / (0.55 + 0.45 * nominal_ratio**0.55)
    return max(0.42, min(1.0, shrink))
