"""Generate figures/hail-traceability-boundary.png at true acmtosem column width.

The canvas is 5.95 inches wide, which is the text width of the acmtosem layout,
so every point size below is the size the reader actually sees in print.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

NAVY = "#12395e"
GREEN = "#1a6440"
GOLD = "#7d5810"
GOLDTXT = "#553b07"
RED = "#98192a"
GREY = "#555e69"

W, H = 5.95, 2.98
X0, CW, GAP = 0.30, 1.05, 0.04
STEP = CW + GAP
CENTRES = [X0 + i * STEP + CW / 2 for i in range(5)]
PX, PW = 0.10, 5.75

fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")


def panel(y, h, edge, face, num, label):
    ax.add_patch(FancyBboxPatch((PX, y), PW, h,
                                boxstyle="round,pad=0.015,rounding_size=0.06",
                                linewidth=0.9, edgecolor=edge, facecolor=face))
    prefix = f"{num}   " if num else ""
    ax.text(PX + 0.12, y + h - 0.15, f"{prefix}{label}", color=edge,
            fontsize=7.6, fontweight="bold", va="center", ha="left")


def box(x, y, w, h, text, edge=NAVY, face="white", fs=7.2, weight="bold",
        tcolor=None, lw=0.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.012,rounding_size=0.05",
                                linewidth=lw, edgecolor=edge, facecolor=face))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight=weight, color=tcolor or NAVY, linespacing=1.35)


def arrow(x1, y, x2, colour=NAVY, ls="-", lw=1.0):
    ax.add_patch(FancyArrowPatch((x1, y), (x2, y), arrowstyle="-|>",
                                 mutation_scale=6.5, linewidth=lw, color=colour,
                                 linestyle=ls, shrinkA=0, shrinkB=0))


ax.text(PX, 2.82, "Instrumentation gaps in the retained CAPRA review trace",
        fontsize=9.6, fontweight="bold", color=NAVY, ha="left", va="center")

# ------------------------------------------------------------------ evaluation context
panel(0.06, 2.38, GOLD, "#fbf8f1", "",
      "EVIDENCE-RECONSTRUCTION VIEW, NOT PIPELINE EXECUTION ORDER")
ax.text(PX + PW - 0.10, 2.16,
        "dashed = cohort connection not retained",
        ha="right", va="center", fontsize=5.9, color=GREY, style="italic")

cy, ch = 1.62, 0.42
stage_x0, stage_w, stage_step = 0.18, 0.72, 0.94
stage_centres = [stage_x0 + i * stage_step + stage_w / 2 for i in range(6)]
for i, c in enumerate(["Artefact\nAI-generated", "Intent\nrationale", "Review\naction",
                       "Revision", "Concordance", "Record"]):
    box(stage_x0 + i * stage_step, cy, stage_w, ch, c,
        edge=GOLD, face="#fdf3dd", fs=6.3,
        tcolor=GOLDTXT)
ymid = cy + ch / 2
for i in range(5):
    x = stage_x0 + i * stage_step
    x1, x2 = x + stage_w + 0.02, x + stage_step - 0.02
    arrow(x1, ymid, x2, colour=RED, ls=(0, (1.6, 1.3)), lw=1.3)
    # an explicit interruption glyph, so the distinction does not rely on
    # dash geometry alone surviving downscaling
    ax.plot([(x1 + x2) / 2], [ymid], marker="|", markersize=4.4, color=RED,
            markeredgewidth=1.1, zorder=6)

for bx, btext in [((stage_centres[1] + stage_centres[2]) / 2,
                   "INTERFACE GAP\nno rationale or\nacknowledgement"),
                  ((stage_centres[3] + stage_centres[4]) / 2,
                   "IDENTITY GAP\nno identifier connects\nrecords across the\nreview path")]:
    ax.plot([bx], [cy - 0.09], marker="X", markersize=4.6, color=RED,
            markeredgecolor="white", markeredgewidth=0.5, zorder=5)
    ax.text(bx, 1.30, btext, ha="center", va="center", fontsize=5.9,
            fontweight="bold", color=RED, linespacing=1.35)

# the emitter is drawn apart from the chain so that no break marker attaches
# to the required-record node itself
box(X0, 0.78, 3.20, 0.24, "Telemetry emitter: produces the records these checks require",
    edge=NAVY, face="#eef5fb", fs=6.0, weight="normal", lw=0.7)
ax.plot([3.66], [0.90], marker="X", markersize=4.6, color=RED,
        markeredgecolor="white", markeredgewidth=0.5, zorder=5)
ax.text(3.80, 0.90, "EMITTER GAP\nrequired dispatch\ntimestamp unavailable", ha="left",
        va="center", fontsize=5.9, fontweight="bold", color=RED, linespacing=1.35)

streams = [("HAIL execution report\n6 successful; both decision branches", GREEN, "#f0f8f3"),
           ("Atlas snapshots\n110 evaluation, 74 feedback documents\nno verified HAIL link", GOLD, "#fdf3dd"),
           ("Corrected-emitter summary\n6 form-triggered, 4 heartbeat records", NAVY, "#eef5fb")]
stw, stgap = 1.75, 0.10
for i, (t, edge, face) in enumerate(streams):
    box(X0 + i * (stw + stgap), 0.42, stw, 0.28, t, edge=edge, face=face,
        fs=5.9, weight="normal", tcolor=edge, lw=0.7)

ax.text(PX + PW / 2, 0.24,
        "Dashed connectors mark cohort connections that cannot be reconstructed from the retained evidence.",
        ha="center", va="center", fontsize=5.5, color=GREY, style="italic",
        linespacing=1.35)

fig.savefig(Path(__file__).resolve().parent / "hail-traceability-boundary.png", dpi=600, facecolor="white")
print("written")
