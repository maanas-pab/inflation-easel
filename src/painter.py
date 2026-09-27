"""Generative still-life painter.

A classic composition — table, cloth, plate, apple, bread loaf,
milk bottle — that visibly degrades with inflation: the apple shrinks,
colours desaturate, craquelure and grain creep in.
"""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle

matplotlib.use("Agg")

CANVAS = (10, 7)


def _backdrop(ax, decay: float = 0.0):
    wall = _fade("#5a4632", decay)
    table = _fade("#7a5c3a", decay)
    cloth = _fade("#ddd3c0", decay)
    ax.add_patch(Rectangle((0, 0), 10, 7, color="#2b2620"))
    ax.add_patch(Rectangle((0, 0), 10, 4.6, color=wall))  # wall
    ax.add_patch(Rectangle((0, 0), 10, 2.4, color=table))  # table
    # table cloth
    ax.add_patch(Polygon([[1, 0], [9, 0], [8.2, 2.4], [1.8, 2.4]], color=cloth))
    # plate shadow + plate
    ax.add_patch(Ellipse((5, 1.55), 5.6, 1.15, color="#00000055"))
    ax.add_patch(Ellipse((5, 1.7), 5.4, 1.05, color="#f2ede0"))
    ax.add_patch(Ellipse((5, 1.7), 4.2, 0.78, color="#d9d2bd"))


def _apple(ax, x, y, r, decay: float = 0.0):
    body = _fade("#c0392b", decay, grey=(0.45, 0.35, 0.3))
    ax.add_patch(Circle((x, y), r, color=body))
    # bruises multiply with decay
    n_bruise = int(decay * 6)
    for i in range(n_bruise):
        ang = (i / max(n_bruise, 1)) * 6.28 + 0.4
        ax.add_patch(Circle((x + r * 0.45 * np.cos(ang), y + r * 0.4 * np.sin(ang)),
                            r * 0.16, color="#4a241833"))
    ax.add_patch(Ellipse((x - r * 0.3, y + r * 0.3), r * 0.7, r * 0.45, color="#ffffff55"))
    ax.plot([x, x + 0.08], [y + r, y + r + 0.35], color="#4a2f1a", lw=3)
    ax.add_patch(Ellipse((x + 0.3, y + r + 0.3), 0.5, 0.22, color=_fade("#3f7a2e", decay)))


def _bread(ax, x, y, w=2.2, h=0.9, decay: float = 0.0):
    crust = _fade("#b57a35", decay)
    crumb = _fade("#d9a45b", decay)
    # stale loaf gets thinner as groceries get dearer
    w = w * (1.0 - 0.25 * decay)
    ax.add_patch(Ellipse((x, y), w, h, color=crust))
    ax.add_patch(Ellipse((x, y + 0.08), w * 0.82, h * 0.62, color=crumb))
    for dx in (-0.5, 0.0, 0.5):
        ax.plot([x + dx - 0.15, x + dx + 0.15], [y + 0.25, y + 0.32], color="#7a4d1c", lw=2)


def _milk(ax, x, y, scale=1.0):
    w, h = 0.9 * scale, 1.9 * scale
    ax.add_patch(Rectangle((x - w / 2, y), w, h, color="#f5f2e8"))
    ax.add_patch(Rectangle((x - w * 0.25, y + h), w * 0.5, 0.35 * scale, color="#d8d2c0"))
    ax.add_patch(Rectangle((x - w / 2, y + h * 0.45), w, h * 0.3, color="#2e6fb0"))


def _fade(hex_color: str, decay: float, grey=(0.5, 0.47, 0.42)):
    """Lerp a hex colour toward warm grey by decay amount."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4))
    k = 0.55 * decay
    return (r + (grey[0] - r) * k, g + (grey[1] - g) * k, b + (grey[2] - b) * k)


def _craquelure(ax, rng, n: int, alpha: float):
    for _ in range(n):
        x0, y0 = rng.uniform(0, 10), rng.uniform(0, 7)
        segs = 4 + int(rng.integers(0, 4))
        xs, ys = [x0], [y0]
        for _ in range(segs):
            xs.append(xs[-1] + rng.normal(0, 0.35))
            ys.append(ys[-1] + rng.normal(0, 0.35))
        ax.plot(xs, ys, color=(0.1, 0.08, 0.06), alpha=min(alpha, 0.55), lw=0.7)


def _grain(ax, rng, amount: float):
    if amount <= 0.01:
        return
    n = int(300 * amount)
    xs = rng.uniform(0, 10, n)
    ys = rng.uniform(0, 7, n)
    ax.scatter(xs, ys, s=rng.uniform(2, 14, n), color=(0.05, 0.04, 0.03),
               alpha=0.08 + 0.15 * amount, linewidths=0)


def paint_still_life(apple_scale: float = 1.0, decay: float = 0.0, seed: int = 7):
    """Draw the composition.

    Args:
        apple_scale: 1.0 in 1970 -> ~0.45 by 2026 (data-driven).
        decay: 0.0 (pristine 1970) -> 1.0 (weathered 2026).
        seed: fixed so the same year always paints the same canvas.
    """
    rng = np.random.default_rng(seed)
    fig, ax = plt.subplots(figsize=CANVAS, dpi=110)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    # decay washes the palette toward grey-brown
    fade = 1.0 - 0.45 * decay
    fig.patch.set_facecolor((0.16 * fade + 0.1 * decay, 0.14 * fade + 0.08 * decay, 0.12 * fade + 0.06 * decay))
    _backdrop(ax, decay)
    _bread(ax, 6.9, 2.35, decay=decay)
    _milk(ax, 2.2, 2.0)
    _apple(ax, 4.6, 2.75, r=1.05 * apple_scale, decay=decay)
    _craquelure(ax, rng, n=int(8 + 70 * decay), alpha=0.12 + 0.4 * decay)
    _grain(ax, rng, amount=decay)
    # empty-plate effect: as decay grows the plate shows more bare china
    ax.text(
        5, 0.35, f"decay {decay:.2f} · apple ×{apple_scale:.2f}",
        ha="center", va="center", fontsize=8, color="#ffffff88",
    )
    fig.tight_layout(pad=0)
    return fig
