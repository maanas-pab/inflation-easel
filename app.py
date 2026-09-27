"""Inflation Easel — drag from 1970 to 2026 and watch the still life decay."""

from __future__ import annotations

import streamlit as st
import pandas as pd

from src.inflation import BASE_YEAR, apple_shrink_factor, load_data, snapshot
from src.painter import paint_still_life

st.set_page_config(page_title="Inflation Easel", page_icon="🍎", layout="wide")

df = load_data()
base = snapshot(df, BASE_YEAR)


def decay_of(snap) -> float:
    lo, hi = float(df["cpi_u"].min()), float(df["cpi_u"].max())
    return float((snap.cpi_u / lo - 1) / (hi / lo - 1))


# ---- header ----
st.title("🍎 Inflation Easel")
st.caption(
    "A classic still life, re-drawn as groceries get expensive. "
    "Drag the slider — the apple shrinks, the bread stales, the varnish cracks."
)

# ---- controls ----
left, right = st.columns([3, 1])
with left:
    year = st.slider("Year", 1970, 2026, 1995, step=1)
    compare = st.checkbox("Compare with 1970 side-by-side", value=True)
with right:
    st.write("")
    st.write("")
    play = st.button("▶ Jump to 2026", use_container_width=True)
    if play:
        year = 2026
    if st.button("↩ Reset to 1970", use_container_width=True):
        year = 1970

snap = snapshot(df, year)
shrink = apple_shrink_factor(snap, df)
decay = decay_of(snap)

# ---- painting ----
if compare:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader(f"{BASE_YEAR} · pristine")
        fig0 = paint_still_life(apple_scale=1.0, decay=0.0, seed=BASE_YEAR)
        st.pyplot(fig0, use_container_width=True)
        st.caption(f"Apple ${base.prices['apples']:.2f}/lb · basket ${base.basket_cost:.2f}")
    with col_b:
        st.subheader(f"{year} · weathered")
        fig = paint_still_life(apple_scale=shrink, decay=decay, seed=year)
        st.pyplot(fig, use_container_width=True)
        tag = "⚠️ projected" if snap.projected else "BLS actuals"
        st.caption(
            f"Apple ${snap.prices['apples']:.2f}/lb (×{snap.prices['apples']/base.prices['apples']:.1f}) "
            f"· basket ${snap.basket_cost:.2f} · {tag}"
        )
else:
    fig = paint_still_life(apple_scale=shrink, decay=decay, seed=year)
    st.pyplot(fig, use_container_width=True)

# ---- metrics ----
m1, m2, m3, m4 = st.columns(4)
m1.metric("🍏 Apple / lb", f"${snap.prices['apples']:.2f}",
          f"{(snap.prices['apples']/base.prices['apples']-1)*100:+.0f}% vs 1970")
m2.metric("🧺 1970 basket today", f"${snap.basket_cost:.2f}",
          f"+${snap.basket_cost - base.basket_cost:.2f}")
m3.metric("📈 Cumulative inflation (CPI-U)", f"{snap.cumulative_inflation*100:.0f}%")
m4.metric("💵 $1 (1970) buys", f"${snap.purchasing_power:.2f} of goods")

# ---- story line ----
if year < 1982:
    st.info("The 1970s: oil shocks and stagflation. Prices climb fast; the varnish barely holds.")
elif year < 2000:
    st.info("The Great Moderation: inflation cools. The apple keeps most of its blush.")
elif year < 2020:
    st.info("Slow and steady: 2%-ish years. The bread thins, cracks spider across the canvas.")
elif year < 2023:
    st.warning("Post-pandemic surge + avian flu: eggs spike 4×. The still life bruises.")
else:
    st.warning("2024-2026: inflation eases but the level stays high. The apple is barely half its 1970 self.")

# ---- charts ----
st.divider()
st.subheader("The data behind the decay")
c1, c2 = st.columns(2)
with c1:
    st.line_chart(df.set_index("year")[["cpi_u"]], height=220)
    st.caption("CPI-U (1982-84 = 100), BLS annual averages. 2025-26 projected.")
with c2:
    prices = df.set_index("year")[["apple_per_lb", "bread_per_loaf", "milk_per_gallon", "eggs_per_dozen"]]
    st.line_chart(prices, height=220)
    st.caption("Nominal grocery prices ($). Eggs tell the volatile story.")

with st.expander("🧾 Basket breakdown (3 lb apples · 2 loaves · 1 gal milk · 1 doz eggs)"):
    row = df[df["year"] == year].iloc[0]
    detail = pd.DataFrame({
        "item": ["apples (3 lb)", "bread (2 loaves)", "milk (1 gal)", "eggs (1 doz)"],
        "1970": [base.prices["apples"]*3, base.prices["bread"]*2, base.prices["milk"], base.prices["eggs"]],
        f"{year}": [row["apple_per_lb"]*3, row["bread_per_loaf"]*2, row["milk_per_gallon"], row["eggs_per_dozen"]],
    })
    st.dataframe(detail.style.format({"1970": "${:.2f}", f"{year}": "${:.2f}"}),
                 use_container_width=True, hide_index=True)

st.divider()
st.caption("Data: U.S. Bureau of Labor Statistics (CPI-U, Food-at-home, Average Price Data). "
           "2025 = YTD average, 2026 = projection. Painting is generative — same year, same canvas.")
