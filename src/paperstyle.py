"""
Shared figure style for the paper: white background, black axes, serif
typography matching the Times-like body text, and a restrained palette in
the tradition of economics journals.
"""
import matplotlib as mpl

# restrained, print-friendly palette
BLUE = "#3268A8"      # dark navy, primary series
CORAL = "#B5443C"     # deep red, contrast / risk series
GOLD = "#D9A21B"      # ochre, highlight series
GREEN = "#3A8A62"     # dark green, secondary series
GRAY = "#8C8C8C"      # neutral / non-significant
INK = "#000000"
SUBTLE = "#404040"
SURFACE = "#FFFFFF"
NAVY = "#000000"      # panel titles in black

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
    "mathtext.fontset": "dejavuserif",
    "text.color": INK,
    "axes.edgecolor": INK, "axes.linewidth": 0.8,
    "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK,
    "xtick.direction": "out", "ytick.direction": "out",
    "xtick.major.size": 3.5, "ytick.major.size": 3.5,
    "axes.grid": False,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": True, "axes.spines.bottom": True,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "font.size": 10,
    "legend.frameon": False,
})
