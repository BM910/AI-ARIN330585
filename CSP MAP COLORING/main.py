"""
main.py — Vietnam CSP Map Colouring (pre-2025, 63 provinces)

Loads province borders from a local GeoJSON, solves the 4-colour CSP
with backtracking + forward checking, then renders the result with matplotlib.

run main.py and result "vietnam_csp_map.png" will be saved in the same folder
"""

import argparse
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import geopandas as gpd

from vietnam_geodata import load_vietnam_geodata, DEFAULT_GEOJSON_PATH


# CONFIGURATION
COLORS: list[str]      = ["#E63946", "#2A9D8F", "#E9C46A", "#457B9D"]
COLOR_NAMES: list[str] = ["Red",     "Teal",    "Yellow",  "Blue"]
OUTPUT_PATH = "vietnam_csp_map.png"


# CLI
parser = argparse.ArgumentParser(description="Vietnam CSP Map Colouring")
parser.add_argument(
    "--geojson", default=DEFAULT_GEOJSON_PATH,
    help="Path to the borders.geojson file (default: %(default)s)",
)
args = parser.parse_args()


# LOAD GEODATA
gdf, neighbors = load_vietnam_geodata(args.geojson)
province_names: list[str] = list(gdf["name"])
n = len(province_names)


def is_consistent(province: str, color: str, assignment: dict[str, str]) -> bool:
    for neighbor in neighbors.get(province, set()):
        if assignment.get(neighbor) == color:
            return False
    return True


def forward_check(province: str, color: str, assignment: dict[str, str]) -> bool:
    for neighbor in neighbors.get(province, set()):
        if neighbor in assignment:
            continue
        if not any(is_consistent(neighbor, c, assignment) for c in COLORS):
            return False
    return True


def select_unassigned(assignment: dict[str, str]) -> str | None:
    for p in province_names:
        if p not in assignment:
            return p
    return None


def backtrack(assignment: dict[str, str]) -> dict[str, str] | None:
    """Recursive backtracking"""
    if len(assignment) == n:
        return assignment

    province = select_unassigned(assignment)
    if province is None:
        return None

    for color in COLORS:
        if is_consistent(province, color, assignment):
            assignment[province] = color
            if forward_check(province, color, assignment):      # FOWARD CHECKING
                result = backtrack(assignment)
                if result is not None:
                    return result
            del assignment[province]

    return None


print("Solving CSP with backtracking + foward checking ...")
solution = backtrack({})

if solution is None:
    print("No solution found – try adding more colours")
    raise SystemExit(1)

colours_used = len(set(solution.values()))
print(f"Solution found using {colours_used} colours\n")
for pname, colour in sorted(solution.items()):
    idx = COLORS.index(colour)
    print(f"   {pname:35s}  →  {COLOR_NAMES[idx]}")


# RENDER WITH MATPLOTLIB
print("\nDrawing map ...")
gdf = gdf.copy()
gdf["color"] = gdf["name"].map(solution)

BACKGROUND = "#1a1a2e"
BORDER_CLR = "#ffffff"

fig, ax = plt.subplots(figsize=(10, 16))
fig.patch.set_facecolor(BACKGROUND)
ax.set_facecolor(BACKGROUND)


# DRAW POLYGONS
for _, row in gdf.iterrows():
    face = row["color"] or "#888888"
    gpd.GeoDataFrame([row], geometry="geometry", crs=gdf.crs).plot(
        ax=ax, color=face, edgecolor=BORDER_CLR, linewidth=0.5, alpha=0.92,
    )


# LABELING
for _, row in gdf.iterrows():
    try:
        cx = row["geometry"].centroid.x
        cy = row["geometry"].centroid.y
        ax.text(
            cx, cy, row["name"],
            fontsize=3.8, ha="center", va="center",
            color="white", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.15", fc=(0, 0, 0, 0.38), lw=0),
        )
    except Exception:
        pass


# TITLE AND AXIS
ax.set_title(
    "Vietnam – CSP Map Colouring\n(63 tỉnh/thành phố, trước sát nhập 2025)",
    color="white", fontsize=15, fontweight="bold", pad=16,
)
ax.axis("off")
plt.tight_layout()


# SAVE
plt.savefig(OUTPUT_PATH, dpi=180, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print(f"\n  Map saved → {OUTPUT_PATH}")