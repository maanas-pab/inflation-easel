"""Smoke test: every year 1970-2026 must paint without errors."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.inflation import apple_shrink_factor, load_data, snapshot
from src.painter import paint_still_life
import matplotlib.pyplot as plt


def test_all_years():
    df = load_data()
    assert len(df) == 57, f"expected 57 rows, got {len(df)}"
    for year in range(1970, 2027):
        snap = snapshot(df, year)
        shrink = apple_shrink_factor(snap, df)
        assert 0.42 <= shrink <= 1.0, (year, shrink)
        decay = (snap.cpi_u / df["cpi_u"].min() - 1) / (df["cpi_u"].max() / df["cpi_u"].min() - 1)
        assert 0.0 <= decay <= 1.0
        fig = paint_still_life(apple_scale=shrink, decay=decay, seed=year)
        plt.close(fig)


if __name__ == "__main__":
    test_all_years()
    print("all 57 years paint OK")
