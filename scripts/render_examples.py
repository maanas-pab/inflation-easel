"""Render example canvases for the README."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.inflation import apple_shrink_factor, load_data, snapshot
from src.painter import paint_still_life

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

df = load_data()
lo, hi = float(df["cpi_u"].min()), float(df["cpi_u"].max())

for year in (1970, 1995, 2026):
    snap = snapshot(df, year)
    shrink = apple_shrink_factor(snap, df)
    decay = (snap.cpi_u / lo - 1) / (hi / lo - 1)
    fig = paint_still_life(apple_scale=shrink, decay=decay, seed=year)
    fig.savefig(OUT / f"still_{year}.png", bbox_inches="tight")
    print(f"wrote still_{year}.png  apple x{shrink:.2f}  decay {decay:.2f}")
