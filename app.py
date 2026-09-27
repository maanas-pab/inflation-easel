"""Inflation Easel — drag from 1970 to 2026 and watch the still life decay."""

import streamlit as st

from src.inflation import apple_shrink_factor, load_data, snapshot
from src.painter import paint_still_life

st.set_page_config(page_title="Inflation Easel", page_icon="🍎", layout="wide")

df = load_data()

st.title("🍎 Inflation Easel")
st.caption("A classic still life, re-drawn as groceries get expensive.")

year = st.slider("Year", 1970, 2026, 1970)
snap = snapshot(df, year)
shrink = apple_shrink_factor(snap, df)
decay = float((snap.cpi_u / df["cpi_u"].min() - 1) / (df["cpi_u"].max() / df["cpi_u"].min() - 1))

fig = paint_still_life(apple_scale=shrink, decay=decay, seed=year)
st.pyplot(fig, use_container_width=True)

c1, c2, c3 = st.columns(3)
c1.metric("Apple (per lb)", f"${snap.prices['apples']:.2f}")
c2.metric("Basket (1970 goods)", f"${snap.basket_cost:.2f}")
c3.metric("Cumulative inflation", f"{snap.cumulative_inflation * 100:.0f}%")
