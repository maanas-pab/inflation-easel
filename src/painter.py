"""Generative still-life painter.

A simple classic composition — table, cloth, plate, apple, bread loaf,
milk bottle — drawn with matplotlib patches. Later commits add the
inflation-driven decay (desaturation, crackle, shrink).
"""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle

matplotlib.use("Agg")

CANVAS = (10, 7)


def _backdrop(ax):
    ax.add_patch(Rectangle((0, 0), 10, 7, color="#2b2620"))
    ax.add_patch(Rectangle((0, 0), 10, 4.6, color="#5a4632"))  # wall
    ax.add_patch(Rectangle((0, 0), 10, 2.4, color="#7a5c3a"))  # table
    # table cloth
    ax.add_patch(Polygon([[1, 0], [9, 0], [8.2, 2.4], [1.8, 2.4]], color="#ddd3c0"))
    # plate shadow + plate
    ax.add_patch(Ellipse((5, 1.55), 5.6, 1.15, color="#00000055"))
    ax.add_patch(Ellipse((5, 1.7), 5.4, 1.05, color="#f2ede0"))
    ax.add_patch(Ellipse((5, 1.7), 4.2, 0.78, color="#d9d2bd"))


def _apple(ax, x, y, r):
    ax.add_patch(Circle((x, y), r, color="#c0392b"))
    ax.add_patch(Ellipse((x - r * 0.3, y + r * 0.3), r * 0.7, r * 0.45, color="#ffffff55"))
    ax.plot([x, x + 0.08], [y + r, y + r + 0.35], color="#4a2f1a", lw=3)
    ax.add_patch(Ellipse((x + 0.3, y + r + 0.3), 0.5, 0.22, color="#3f7a2e"))


def _bread(ax, x, y, w=2.2, h=0.9):
    ax.add_patch(Ellipse((x, y), w, h, color="#b57a35"))
    ax.add_patch(Ellipse((x, y + 0.08), w * 0.82, h * 0.62, color="#d9a45b"))
    for dx in (-0.5, 0.0, 0.5):
        ax.plot([x + dx - 0.15, x + dx + 0.15], [y + 0.25, y + 0.32], color="#7a4d1c", lw=2)


def _milk(ax, x, y, scale=1.0):
    w, h = 0.9 * scale, 1.9 * scale
    ax.add_patch(Rectangle((x - w / 2, y), w, h, color="#f5f2e8"))
    ax.add_patch(Rectangle((x - w * 0.25, y + h), w * 0.5, 0.35 * scale, color="#d8d2c0"))
    ax.add_patch(Rectangle((x - w / 2, y + h * 0.45), w, h * 0.3, color="#2e6fb0"))


def paint_still_life(apple_scale: float = 1.0):
    """Draw the base composition. apple_scale 1.0 = 1970 apple."""
    fig, ax = plt.subplots(figsize=CANVAS, dpi=110)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    _backdrop(ax)
    _bread(ax, 6.9, 2.35)
    _milk(ax, 2.2, 2.0)
    _apple(ax, 4.6, 2.75, r=1.05 * apple_scale)
    fig.tight_layout(pad=0)
    return fig
