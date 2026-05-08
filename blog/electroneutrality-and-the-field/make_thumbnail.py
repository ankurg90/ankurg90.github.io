"""Catchy Gauss's-law thumbnail for the blog post.

Renders a soft cream background with a dashed circular Gaussian
surface, a small cloud of + and - charges, field lines drifting
outward, and a friendly title overlay. Saved as 1200x630 PNG suitable
for OpenGraph / Twitter card.
"""
from __future__ import annotations
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow

mpl.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
    "savefig.dpi": 200,
})

W, H = 12.0, 6.3   # inches; final 2400x1260 -> resized to 1200x630
fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor("#fafaf8")
ax.set_facecolor("#fafaf8")
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.axis("off")

# ---- Gaussian surface ---------------------------------------------------
gx, gy = 4.2, 3.15
gR = 1.95
gauss = Circle((gx, gy), gR, fill=False, ec="#1e2a3a",
               lw=2.5, ls=(0, (6, 4)))
ax.add_patch(gauss)
# Faint fill
ax.add_patch(Circle((gx, gy), gR, fc="#dbeafe", ec="none", alpha=0.35))

# Label "Gaussian surface" above the circle
ax.text(gx, gy + gR + 0.35, "Gaussian surface",
        ha="center", va="bottom",
        fontsize=14, color="#1e2a3a",
        fontfamily="DejaVu Sans", fontweight="600")

# ---- Charges inside the surface ----------------------------------------
# Net positive: 4 +, 2 - inside
rng = np.random.default_rng(7)
pos = []
def add_charge(x, y, sign):
    pos.append((x, y, sign))

# Place charges on a small ring + center
add_charge(gx - 0.55, gy + 0.30, +1)
add_charge(gx + 0.45, gy + 0.50, +1)
add_charge(gx + 0.65, gy - 0.25, +1)
add_charge(gx - 0.65, gy - 0.30, +1)
add_charge(gx - 0.10, gy - 0.55, -1)
add_charge(gx + 0.05, gy + 0.15, -1)

for (x, y, s) in pos:
    color = "#dc2626" if s > 0 else "#2563eb"
    ax.add_patch(Circle((x, y), 0.18, fc=color, ec="white", lw=2, zorder=5))
    ax.text(x, y, "+" if s > 0 else "−",
            ha="center", va="center",
            fontsize=15, color="white", fontweight="bold", zorder=6)

# ---- Field lines emerging radially -------------------------------------
n_lines = 18
for k in range(n_lines):
    th = 2 * np.pi * k / n_lines
    r0 = gR + 0.05
    r1 = gR + 1.55
    # Curved a bit by adding tiny tangential variation for visual softness
    rs = np.linspace(r0, r1, 30)
    xs = gx + rs * np.cos(th)
    ys = gy + rs * np.sin(th)
    ax.plot(xs, ys, color="#dc262699", lw=1.4, solid_capstyle="round")
    # Small arrow head
    head = 0.12
    ax.annotate("",
                xy=(xs[-1], ys[-1]),
                xytext=(xs[-3], ys[-3]),
                arrowprops=dict(arrowstyle="-|>",
                                color="#dc2626",
                                lw=1.4, mutation_scale=10),
                zorder=4)

# ---- Right-hand title block --------------------------------------------
tx = 7.65   # title left margin
ax.text(tx, 4.85,
        "Electroneutrality",
        ha="left", va="bottom",
        fontsize=32, color="#1e2a3a",
        fontfamily="DejaVu Sans", fontweight="700",
        )
ax.text(tx, 4.40,
        "and the electric field",
        ha="left", va="bottom",
        fontsize=20, color="#1e2a3a",
        fontfamily="DejaVu Sans", fontweight="500",
        fontstyle="italic")

# Tagline / equation
ax.text(tx, 3.4,
        "$\\oint \\mathbf{E}\\!\\cdot\\!d\\mathbf{A} = Q_{\\rm enc}/\\varepsilon$",
        ha="left", va="center",
        fontsize=22, color="#2563eb")
ax.text(tx, 2.55,
        "constant field $\\Rightarrow$ electroneutral,",
        ha="left", va="center",
        fontsize=13, color="#1e2a3a",
        fontfamily="DejaVu Sans")
ax.text(tx, 2.1,
        "but the converse fails.",
        ha="left", va="center",
        fontsize=13, color="#1e2a3a",
        fontfamily="DejaVu Sans", fontweight="600")

# Subtle horizontal divider between art and title
ax.plot([7.20, 7.20], [0.7, 5.6], color="#1e2a3a", lw=0.8, alpha=0.18)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
out = "/Users/angu1560/Dropbox/Boulder/LIFE students/Claude projects/20260405 electrophoresis deformed sphere/website/assets/og-electroneutrality.png"
fig.savefig(out, dpi=200, bbox_inches=None, facecolor="#fafaf8", pad_inches=0)
plt.close(fig)

# Verify dimensions
from PIL import Image
img = Image.open(out)
print(f"Saved: {out}")
print(f"Dimensions: {img.size[0]} x {img.size[1]}")
# Resize to exactly 1200x630 if larger
if img.size != (1200, 630):
    img = img.resize((1200, 630), Image.LANCZOS)
    img.save(out)
    print(f"Resized to 1200x630")
