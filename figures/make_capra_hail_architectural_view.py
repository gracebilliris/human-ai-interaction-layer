"""Generate figures/capra-hail-architectural-view.png at true acmtosem column width.

The canvas is 5.95 inches wide, the text width of the acmtosem layout, so every
point size below is the size the reader sees in print.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

NAVY = "#2c3e57"
GREY = "#5b6470"
PURPLE = "#6b3fa0"
SLATE = "#7b8794"

W, H = 5.95, 3.58
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

BW, BGAP, BX0 = 0.72, 0.13, 0.90
BY, BH = 2.02, 0.60
CENTRES = [BX0 + i * (BW + BGAP) + BW / 2 for i in range(5)]

stages = [("Data\nFederation", "federate, normalise", "#dbe7f6", "#3f6fa8"),
          ("Context\nProcessing", "enrich, prepare", "#c9dcf2", "#3f6fa8"),
          ("Risk\nIntelligence", "assess, propose", "#fbeccb", "#b08422"),
          ("Feedback and\nRefinement", "incorporate review", "#d8eede", "#3f8a5c"),
          ("HAIL", "review checkpoint", "#eadcf5", PURPLE)]


def rbox(x, y, w, h, edge, face, lw=0.8, ls="solid", z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.012,rounding_size=0.045",
                                linewidth=lw, edgecolor=edge, facecolor=face,
                                linestyle=ls, zorder=z))


def arrow(x1, y1, x2, y2, colour=NAVY, lw=1.0, ls="-", z=4, ms=6.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=ms, linewidth=lw, color=colour,
                                 linestyle=ls, shrinkA=0, shrinkB=0, zorder=z))


ax.text(0.06, 3.42, "CAPRA pipeline with an integrated HAIL review checkpoint", fontsize=9.2,
        fontweight="bold", color=NAVY, ha="left", va="center")
ax.text(0.06, 3.24, "Study-specific view of the implemented pipeline over the shared Context Layer substrate",
        fontsize=6.2, color=GREY, ha="left", va="center")

# CAPRA system boundary
rbox(0.80, 0.42, 4.34, 2.62, NAVY, "#f7f9fc", lw=1.0, z=1)
ax.text(0.90, 2.92, "CAPRA SYSTEM BOUNDARY", fontsize=6.2, fontweight="bold",
        color=NAVY, ha="left", va="center", zorder=3)

ax.text((CENTRES[0] + CENTRES[2]) / 2, 2.74, "IMPLEMENTED PIPELINE", fontsize=5.6,
        fontweight="bold", color=GREY, ha="center", va="center", zorder=3)

# external systems and human reviewer, outside the boundary
rbox(0.06, BY, 0.66, BH, SLATE, "#f2f4f7")
ax.text(0.39, BY + 0.45, "External\nsystems", fontsize=6.0, fontweight="bold",
        color=NAVY, ha="center", va="center", linespacing=1.25, zorder=3)
ax.text(0.39, BY + 0.17, "Operational data\nand source APIs", fontsize=5.0,
        color=NAVY, ha="center", va="center", linespacing=1.35, zorder=3)
rbox(5.23, BY, 0.66, BH, SLATE, "#f2f4f7")
ax.text(5.56, BY + 0.45, "Human\nreviewer", fontsize=6.0, fontweight="bold",
        color=NAVY, ha="center", va="center", linespacing=1.25, zorder=3)
ax.text(5.56, BY + 0.17, "Review action\nand feedback", fontsize=5.0,
        color=NAVY, ha="center", va="center", linespacing=1.35, zorder=3)

# pipeline stages
for i, (name, role, face, edge) in enumerate(stages):
    x = BX0 + i * (BW + BGAP)
    rbox(x, BY, BW, BH, edge, face, z=3)
    ax.text(x + BW / 2, BY + 0.42, name, fontsize=6.0, fontweight="bold",
            color=NAVY, ha="center", va="center", linespacing=1.25, zorder=4)
    ax.add_line(Line2D([x + 0.08, x + BW - 0.08], [BY + 0.23, BY + 0.23],
                       color=edge, linewidth=0.5, zorder=4))
    ax.text(x + BW / 2, BY + 0.13, role, fontsize=5.0, color=GREY,
            ha="center", va="center", zorder=4)
    if i < 4:
        arrow(x + BW + 0.012, BY + BH / 2, x + BW + BGAP - 0.012, BY + BH / 2, lw=1.1)

arrow(0.72, BY + BH / 2, BX0 - 0.012, BY + BH / 2, lw=1.1)
ax.text(0.81, BY + BH / 2 + 0.10, "ingest", fontsize=5.0, color=GREY,
        ha="center", va="center", style="italic", zorder=6,
        bbox=dict(facecolor="white", edgecolor="none", pad=0.4))
ax.add_patch(FancyArrowPatch((BX0 + 4 * (BW + BGAP) + BW + 0.012, BY + BH / 2),
                             (5.218, BY + BH / 2), arrowstyle="<|-|>",
                             mutation_scale=6.0, linewidth=1.1, color=NAVY,
                             shrinkA=0, shrinkB=0, zorder=4))

# human review action returns from HAIL into Feedback and Refinement
ax.add_line(Line2D([CENTRES[4], CENTRES[4]], [BY, 1.80], color=PURPLE,
                   linewidth=0.9, zorder=5))
ax.add_line(Line2D([CENTRES[3], CENTRES[4]], [1.80, 1.80], color=PURPLE,
                   linewidth=0.9, zorder=5))
arrow(CENTRES[3], 1.80, CENTRES[3], BY - 0.008, colour=PURPLE, lw=0.9, z=5)
ax.text((CENTRES[3] + CENTRES[4]) / 2, 1.72, "human review action", fontsize=5.0,
        color=PURPLE, ha="center", va="center", style="italic", zorder=5)

# shared Context Layer substrate
rbox(0.90, 0.56, 4.12, 0.78, "#8b93a1", "#eceff4", z=2)
ax.text(0.99, 1.22, "Context Layer", fontsize=7.0, fontweight="bold",
        color=NAVY, ha="left", va="center", zorder=3)
ax.text(0.99, 1.11, "Shared substrate, not a pipeline stage", fontsize=5.2,
        color=GREY, ha="left", va="center", style="italic", zorder=3)
rbox(1.26, 0.64, 3.40, 0.26, "#b6bdc9", "white", lw=0.7, z=3)
ax.text(2.96, 0.77, "Shared records and services", fontsize=6.1,
        fontweight="bold", color=NAVY, ha="center", va="center", zorder=4)

for c in CENTRES:
    ax.add_line(Line2D([c, c], [BY, 1.40], color="#8b93a1", linewidth=0.7,
                       linestyle=(0, (2.2, 1.6)), zorder=2))
    ax.plot([c], [1.38], marker="o", markersize=1.8, color="#8b93a1", zorder=3)
ax.text((CENTRES[1] + CENTRES[2]) / 2, 1.49, "shared context services and records",
        fontsize=5.0, color=GREY, ha="center", va="center", style="italic",
        zorder=6, bbox=dict(facecolor="white", edgecolor="none", pad=0.8))

# legend
ly = 0.20
ax.add_line(Line2D([0.10, 0.30], [ly, ly], color=NAVY, linewidth=1.1))
arrow(0.28, ly, 0.32, ly, lw=1.1)
ax.text(0.36, ly, "primary pipeline flow", fontsize=5.2, color=GREY, va="center")
ax.add_line(Line2D([1.42, 1.66], [ly, ly], color="#8b93a1", linewidth=0.7,
                   linestyle=(0, (2.2, 1.6))))
ax.text(1.71, ly, "shared-substrate access", fontsize=5.2, color=GREY, va="center")
ax.add_line(Line2D([2.80, 3.04], [ly, ly], color=PURPLE, linewidth=1.0,
                   linestyle="-"))
ax.text(3.09, ly, "human review return flow", fontsize=5.2, color=GREY, va="center")

fig.savefig(Path(__file__).resolve().parent / "capra-hail-architectural-view.png", dpi=600, facecolor="white")
print("written")
