"""Generate a print-sized overview of HAIL's review checkpoint and return contract."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

NAVY = "#193b63"
GREY = "#596473"
PURPLE = "#6b3fa0"
GREEN = "#1f6b45"
BLUE_FILL = "#eaf1f8"
PURPLE_FILL = "#f0e7f7"
GREEN_FILL = "#e9f4ed"

W, H = 6.65, 2.85
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")


def box(x, y, width, height, edge, face, radius=0.045, linewidth=0.9):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle=f"round,pad=0.012,rounding_size={radius}",
            linewidth=linewidth,
            edgecolor=edge,
            facecolor=face,
        )
    )


def arrow(x1, y1, x2, y2, colour=NAVY, linewidth=1.0, style="-|>"):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle=style,
            mutation_scale=6.5,
            linewidth=linewidth,
            color=colour,
            shrinkA=0,
            shrinkB=0,
        )
    )


ax.text(
    0.08,
    2.68,
    "HAIL review checkpoint and return contract",
    fontsize=9.2,
    fontweight="bold",
    color=NAVY,
    ha="left",
    va="center",
)
ax.text(
    0.08,
    2.48,
    "The review action returns to the agentic pipeline with the artefact and review identity connected.",
    fontsize=5.9,
    color=GREY,
    ha="left",
    va="center",
)

# External pipeline components.
box(0.08, 1.05, 1.08, 0.82, NAVY, BLUE_FILL)
ax.text(0.62, 1.66, "Upstream\nAI agent", fontsize=6.5, fontweight="bold",
        color=NAVY, ha="center", va="center", linespacing=1.2)
ax.text(0.62, 1.29, "artefact, context,\nactions, review ID", fontsize=5.0,
        color=GREY, ha="center", va="center", linespacing=1.25)

box(5.52, 1.05, 1.05, 0.82, GREEN, GREEN_FILL)
ax.text(6.045, 1.66, "Downstream\nagent", fontsize=6.5, fontweight="bold",
        color=NAVY, ha="center", va="center", linespacing=1.2)
ax.text(6.045, 1.29, "refinement and\ndecision recording", fontsize=5.0,
        color=GREY, ha="center", va="center", linespacing=1.25)

# HAIL boundary.
box(1.34, 0.62, 4.02, 1.60, PURPLE, "#fbf8fd", radius=0.06, linewidth=1.0)
ax.text(1.49, 2.07, "HAIL", fontsize=7.0, fontweight="bold", color=PURPLE,
        ha="left", va="center")

stages = [
    (1.54, "Receive\nreview request", "connected input"),
    (2.48, "Present artefact\nand context", "review interface"),
    (3.42, "Capture review\naction", "review action"),
    (4.36, "Return connected\naction", "review ID preserved"),
]

for x, title, detail in stages:
    box(x, 1.10, 0.82, 0.72, PURPLE, PURPLE_FILL, radius=0.035, linewidth=0.75)
    ax.text(x + 0.41, 1.59, title, fontsize=5.35, fontweight="bold",
            color=NAVY, ha="center", va="center", linespacing=1.15)
    ax.text(x + 0.41, 1.25, detail, fontsize=4.5, color=GREY,
            ha="center", va="center")

for left in (2.36, 3.30, 4.24):
    arrow(left, 1.46, left + 0.10, 1.46, colour=PURPLE, linewidth=0.9)

arrow(1.16, 1.46, 1.52, 1.46)
arrow(5.20, 1.46, 5.50, 1.46, colour=GREEN)

# Human reviewer interaction.
box(2.49, 0.08, 1.78, 0.38, NAVY, "#f3f5f7", radius=0.035, linewidth=0.75)
ax.text(3.38, 0.27, "Human reviewer", fontsize=5.9, fontweight="bold",
        color=NAVY, ha="center", va="center")
arrow(2.89, 1.10, 2.89, 0.48, colour=NAVY, linewidth=0.85)
arrow(3.83, 0.48, 3.83, 1.10, colour=PURPLE, linewidth=0.85)
ax.text(2.67, 0.78, "present", fontsize=4.5, color=GREY, ha="center")
ax.text(4.05, 0.78, "review", fontsize=4.5, color=PURPLE, ha="center")

fig.savefig(Path(__file__).resolve().parent / "hail-review-checkpoint.png", dpi=600, facecolor="white")
print("written")
