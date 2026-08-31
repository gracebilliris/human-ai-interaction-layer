"""Generate the introductory review-chain traceability figure at ACM column width."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

NAVY = "#12395e"
GREEN = "#1a6440"
RED = "#98192a"
GREY = "#555e69"

W, H = 5.95, 3.18
X0, BW, GAP = 0.76, 0.82, 0.18
STEP = BW + GAP

fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")


def box(x, y, title, detail, edge, face, w=BW):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            0.62,
            boxstyle="round,pad=0.012,rounding_size=0.05",
            linewidth=0.9,
            edgecolor=edge,
            facecolor=face,
            zorder=2,
        )
    )
    ax.text(
        x + w / 2,
        y + 0.43,
        title,
        ha="center",
        va="center",
        fontsize=6.5,
        fontweight="bold",
        color=edge,
        zorder=3,
    )
    ax.text(
        x + w / 2,
        y + 0.20,
        detail,
        ha="center",
        va="center",
        fontsize=5.0,
        color=NAVY,
        linespacing=1.2,
        zorder=3,
    )


def arrow(x1, y, x2, colour, dashed=False):
    style = (0, (2.0, 1.7)) if dashed else "-"
    ax.add_patch(
        FancyArrowPatch(
            (x1, y),
            (x2, y),
            arrowstyle="-|>",
            mutation_scale=5.8,
            linewidth=1.2,
            color=colour,
            linestyle=style,
            shrinkA=0,
            shrinkB=0,
            zorder=4,
        )
    )
    if dashed:
        ax.plot(
            [(x1 + x2) / 2],
            [y],
            marker="|",
            markersize=5.0,
            color=RED,
            markeredgewidth=1.2,
            zorder=5,
        )


stages = [
    ("Intent", "review\nrationale"),
    ("Review", "human review\naction"),
    ("Revision", "updated\nartefact"),
    ("Concordance", "human–AI\naction comparison"),
    ("Record", "decision\nrecord"),
]

ax.text(
    0.10,
    3.02,
    "Traceability across a human review path",
    fontsize=9.4,
    fontweight="bold",
    color=NAVY,
    ha="left",
    va="center",
)
ax.text(
    0.10,
    2.78,
    "Evidence-reconstruction order, not pipeline execution order.",
    fontsize=6.1,
    color=GREY,
    ha="left",
    va="center",
)

rows = [
    (1.72, "RECONSTRUCTABLE REVIEW", GREEN, GREEN, "#f0f8f3", set(), stages),
    (
        0.67,
        "INCOMPLETE EVIDENCE",
        RED,
        NAVY,
        "#f3f6f9",
        {0, 1, 2, 3},
        [
            ("Intent", "rationale\nnot retained"),
            ("Review", "human review\naction"),
            ("Revision", "updated\nartefact"),
            ("Concordance", "human–AI\naction comparison"),
            ("Record", "decision\nrecord"),
        ],
    ),
]

for y, label, label_colour, box_edge, face, broken_after, row_stages in rows:
    ax.text(
        0.10,
        y + 0.78,
        label,
        fontsize=6.2,
        fontweight="bold",
        color=label_colour,
        ha="left",
        va="center",
    )
    box(0.08, y, "Artefact", "AI-generated", NAVY, "#eef5fb", w=0.54)
    entry_broken = label == "INCOMPLETE EVIDENCE"
    arrow(
        0.635,
        y + 0.31,
        X0 - 0.015,
        RED if entry_broken else GREEN,
        dashed=entry_broken,
    )
    for i, (title, detail) in enumerate(row_stages):
        x = X0 + i * STEP
        box(x, y, title, detail, box_edge, face)
        if i < len(row_stages) - 1:
            arrow(
                x + BW + 0.015,
                y + 0.31,
                x + STEP - 0.015,
                RED if i in broken_after else GREEN,
                dashed=i in broken_after,
            )

ax.add_line(Line2D([0.18, 0.43], [0.38, 0.38], color=GREEN, linewidth=1.2))
ax.text(0.49, 0.38, "reconstructable connection", fontsize=5.4, color=GREY, va="center")
ax.add_line(
    Line2D(
        [1.72, 1.97],
        [0.38, 0.38],
        color=RED,
        linewidth=1.2,
        linestyle=(0, (2.0, 1.7)),
    )
)
ax.plot([1.845], [0.38], marker="|", markersize=5.0, color=RED, markeredgewidth=1.2)
ax.text(2.03, 0.38, "connection not reconstructable from retained evidence", fontsize=5.4, color=GREY, va="center")
ax.text(
    W / 2,
    0.13,
    "Dashed connections mark relationships that cannot be reconstructed from the retained evidence.",
    fontsize=5.35,
    color=GREY,
    style="italic",
    ha="center",
    va="center",
)

fig.savefig(Path(__file__).resolve().parent / "review-chain-traceability.png", dpi=600, facecolor="white")
print("written")
