import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arc, Circle, Wedge
from matplotlib.path import Path
import matplotlib.patheffects as pe
import matplotlib.transforms as transforms
import numpy as np

# ─── Canvas Setup ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 10), facecolor='#0A0E1A')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('#0A0E1A')

# ─── Color Palette ────────────────────────────────────────────────────────────
BG        = '#0A0E1A'
DARK      = '#0D1117'
CYAN      = '#00F5FF'
GREEN     = '#39FF14'
PURPLE    = '#BF5FFF'
ORANGE    = '#FF6B35'
WHITE     = '#FFFFFF'
DIM_CYAN  = '#003D4D'
DIM_GREEN = '#0D2600'
GOLD      = '#FFD700'

# ─── Helper: draw glowing text ───────────────────────────────────────────────
def glow_text(x, y, s, color, size, alpha=0.25, **kwargs):
    for glow_size, glow_alpha in [(size+10, alpha*0.3), (size+5, alpha*0.6), (size, 1.0)]:
        ax.text(x, y, s, color=color, fontsize=glow_size,
                ha='center', va='center', **kwargs,
                path_effects=[pe.withStroke(linewidth=6 if glow_size > size else 0,
                                             foreground=color,
                                             alpha=glow_alpha if glow_size > size else 1)])

# ─── 1. Outer Ring — Orbit ────────────────────────────────────────────────────
for r, lw, col, a in [(38, 0.5, CYAN, 0.15), (36, 1.2, CYAN, 0.35), (34.5, 2.5, CYAN, 0.6)]:
    circle = plt.Circle((50, 52), r, fill=False, edgecolor=col, linewidth=lw, alpha=a)
    ax.add_patch(circle)

# ─── 2. Inner Glow Circle ────────────────────────────────────────────────────
for r, a in [(28, 0.04), (24, 0.07), (20, 0.10)]:
    glow = plt.Circle((50, 52), r, color=CYAN, alpha=a)
    ax.add_patch(glow)

# ─── 3. Hexagon Border ───────────────────────────────────────────────────────
def hexagon(cx, cy, r, color, lw, alpha=1.0):
    angles = [math.radians(60*i + 30) for i in range(7)]
    xs = [cx + r * math.cos(a) for a in angles]
    ys = [cy + r * math.sin(a) for a in angles]
    ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha)

hexagon(50, 52, 32, CYAN,   0.4, 0.2)
hexagon(50, 52, 30, CYAN,   1.0, 0.4)
hexagon(50, 52, 28, PURPLE, 2.0, 0.7)

# ─── 4. Corner Tick Marks on outer ring ──────────────────────────────────────
tick_angles = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
for angle_deg in tick_angles:
    a = math.radians(angle_deg)
    inner_r, outer_r = 33.5, 36.5
    x1, y1 = 50 + inner_r * math.cos(a), 52 + inner_r * math.sin(a)
    x2, y2 = 50 + outer_r * math.cos(a), 52 + outer_r * math.sin(a)
    lw = 2.0 if angle_deg % 90 == 0 else 1.0
    ax.plot([x1, x2], [y1, y2], color=CYAN, linewidth=lw, alpha=0.7)

# ─── 5. Central Dark Disc ────────────────────────────────────────────────────
disc = plt.Circle((50, 52), 26, color=DARK, zorder=2)
ax.add_patch(disc)
disc2 = plt.Circle((50, 52), 26, fill=False, edgecolor=PURPLE, linewidth=1.5, alpha=0.5, zorder=3)
ax.add_patch(disc2)

# ─── 6. Binary Rain (background decoration) ──────────────────────────────────
np.random.seed(42)
for _ in range(60):
    bx = np.random.uniform(2, 98)
    by = np.random.uniform(2, 98)
    dist = math.hypot(bx - 50, by - 52)
    if dist > 30:
        bit = np.random.choice(['0', '1'])
        alpha = np.random.uniform(0.05, 0.18)
        size  = np.random.uniform(5, 9)
        ax.text(bx, by, bit, color=GREEN, fontsize=size, alpha=alpha,
                ha='center', va='center',
                fontfamily='monospace', fontweight='bold')

# ─── 7. Orbiting Code Symbols ────────────────────────────────────────────────
orbit_symbols = [
    (0,   '{ }',  CYAN,   11),
    (45,  '</>',  GREEN,  10),
    (90,  '( )',  PURPLE, 11),
    (135, '[ ]',  ORANGE, 10),
    (180, '{ }',  CYAN,   11),
    (225, '>>',   GREEN,   9),
    (270, '##',   PURPLE, 10),
    (315, '::',   ORANGE, 10),
]

orbit_r = 43
for angle_deg, sym, col, sz in orbit_symbols:
    a = math.radians(angle_deg)
    sx = 50 + orbit_r * math.cos(a)
    sy = 52 + orbit_r * math.sin(a)
    # glow backing
    ax.text(sx, sy, sym, color=col, fontsize=sz+4, ha='center', va='center',
            fontfamily='monospace', fontweight='bold', alpha=0.2, zorder=1)
    ax.text(sx, sy, sym, color=col, fontsize=sz, ha='center', va='center',
            fontfamily='monospace', fontweight='bold', alpha=0.9, zorder=4)

# ─── 8. Main Bracket Symbol: </> ─────────────────────────────────────────────
ax.text(50, 57.5, '</>',
        color=CYAN,
        fontsize=42,
        ha='center',
        va='center',
        fontfamily='monospace',
        fontweight='bold',
        zorder=8,
        path_effects=[
            pe.withStroke(linewidth=18, foreground=CYAN, alpha=0.08),
            pe.withStroke(linewidth=8, foreground=CYAN, alpha=0.18),
        ])

# Full </> as a single layered text for correct spacing
for dx, col, alpha, sz in [(0, CYAN, 0.15, 42), (0, CYAN, 1.0, 38)]:
    pass  # already drawn above

ax.text(50, 56.5, '</>',
        color=CYAN, fontsize=40, ha='center', va='center',
        fontfamily='monospace', fontweight='black', alpha=0.0, zorder=7)

# Redraw cleanly as one unit
ax.text(50, 57, '</>', color='white', fontsize=36,
        ha='center', va='center', fontfamily='monospace', fontweight='bold',
        alpha=0, zorder=8)

# Clean single draw
ax.text(50, 57.5, '</>',
        color=CYAN, fontsize=37, ha='center', va='center',
        fontfamily='monospace', fontweight='bold', zorder=8,
        path_effects=[
            pe.withStroke(linewidth=12, foreground=CYAN, alpha=0.12),
            pe.withStroke(linewidth=5, foreground=CYAN, alpha=0.3),
        ])

# ─── 9. Club Name — "CODE" ────────────────────────────────────────────────────
ax.text(50, 43, 'CODING CLUB', color=WHITE, fontsize=18, ha='center', va='center',
        fontfamily='monospace', fontweight='bold', zorder=9,
        path_effects=[pe.withStroke(linewidth=4, foreground=CYAN, alpha=0.5)])

# Underline
ax.plot([35, 65], [41.2, 41.2], color=CYAN, linewidth=1.5, alpha=0.6, zorder=9)

# ─── 10. "CLUB" Subtitle ─────────────────────────────────────────────────────
ax.text(50, 39.5, '', color=WHITE, fontsize=11, ha='center', va='center',
        fontfamily='monospace', fontweight='bold', zorder=9, alpha=0.9)

# ─── 11. Bottom Tagline Arc Text (simulated with flat text) ──────────────────
ax.text(50, 21, '>> CREATE  ·  COMPILE <<',
        color=WHITE, fontsize=7.5, ha='center', va='center',
        fontfamily='monospace', alpha=0.7, zorder=4)

# ─── 12. Top arc label ───────────────────────────────────────────────────────
ax.text(50, 83, '» CSE  ·  2026 «',
        color=WHITE, fontsize=7, ha='center', va='center',
        fontfamily='monospace', alpha=0.75, zorder=4)

# ─── 13. Corner bracket decorations ─────────────────────────────────────────
bracket_color = CYAN
bw, bh, bl = 6, 6, 1.8  # width, height, linewidth

def corner_bracket(cx, cy, flip_x=False, flip_y=False):
    sx = -1 if flip_x else 1
    sy = -1 if flip_y else 1
    ax.plot([cx, cx + sx*bw], [cy + sy*bh, cy + sy*bh], color=bracket_color, lw=bl, alpha=0.6)
    ax.plot([cx, cx], [cy, cy + sy*bh], color=bracket_color, lw=bl, alpha=0.6)

corner_bracket(4, 4)
corner_bracket(96, 4, flip_x=True)
corner_bracket(4, 96, flip_y=True)
corner_bracket(96, 96, flip_x=True, flip_y=True)

# ─── 14. Scanline subtle effect ──────────────────────────────────────────────
for y_line in range(0, 100, 4):
    ax.axhline(y=y_line, color='#FFFFFF', linewidth=0.2, alpha=0.015, zorder=0)

# ─── 15. Connecting lines from outer symbols to ring ─────────────────────────
for angle_deg in [0, 90, 180, 270]:
    a = math.radians(angle_deg)
    x1, y1 = 50 + 36.8 * math.cos(a), 52 + 36.8 * math.sin(a)
    x2, y2 = 50 + 40.5 * math.cos(a), 52 + 40.5 * math.sin(a)
    ax.plot([x1, x2], [y1, y2], color=GREEN, linewidth=2, alpha=0.5, zorder=3)

# ─── Save ────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0)
plt.savefig('codelogo.png',
            dpi=300,
            bbox_inches='tight',
            facecolor=BG,
            edgecolor='none')
print("✅ Logo saved to codelogo.png")
plt.close()
