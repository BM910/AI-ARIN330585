"""
Github Link: github.com/BM910/AI-ARIN330585

main.py — Vietnam CSP Map Colouring (pre-2025, 63 provinces)

Loads province borders from a local GeoJSON, then solves the 4-colour CSP
THREE different ways:

  1. Backtracking + Forward Checking
  2. AC-3 (arc consistency) preprocessing, then Backtracking + Forward Checking
  3. Min-Conflicts (local search)

Each approach is rendered with matplotlib and saved as its own PNG.
No CLI flags needed — just run main.py and all three images are produced
in the same folder:

    vietnam_csp_map_backtracking.png
    vietnam_csp_map_ac3_backtracking.png
    vietnam_csp_map_min_conflicts.png
"""

import time

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import geopandas as gpd

from vietnam_geodata import load_vietnam_geodata, DEFAULT_GEOJSON_PATH
from solvers import backtracking_search, ac3_then_backtracking, min_conflicts


# CONFIGURATION
COLORS: list[str]      = ["#E63946", "#2A9D8F", "#E9C46A", "#457B9D"]
COLOR_NAMES: list[str] = ["Red",     "Teal",    "Yellow",  "Blue"]

BACKGROUND = "#1a1a2e"
BORDER_CLR = "#ffffff"


# RENDERING
def render_map(gdf: gpd.GeoDataFrame, solution: dict[str, str],
                title: str, output_path: str) -> None:
    """Draw provinces coloured by `solution` and save to `output_path`."""
    gdf = gdf.copy()
    gdf["color"] = gdf["name"].map(solution)

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
    ax.set_title(title, color="white", fontsize=15, fontweight="bold", pad=16)
    ax.axis("off")
    plt.tight_layout()

    # SAVE
    plt.savefig(output_path, dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"   Map saved → {output_path}")


def print_solution(solution: dict[str, str]) -> None:
    colours_used = len(set(solution.values()))
    print(f"   Colours used: {colours_used}")
    for pname, colour in sorted(solution.items()):
        idx = COLORS.index(colour)
        print(f"      {pname:35s}  →  {COLOR_NAMES[idx]}")


# ──────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────
def main() -> None:
    gdf, neighbors = load_vietnam_geodata(DEFAULT_GEOJSON_PATH)
    province_names: list[str] = list(gdf["name"])

    # ── 1. BACKTRACKING + FORWARD CHECKING ──────────────────────────────
    print("=" * 70)
    print("1) Solving with Backtracking + Forward Checking ...")
    t0 = time.perf_counter()
    bt_solution = backtracking_search(province_names, COLORS, neighbors)
    bt_time = time.perf_counter() - t0

    if bt_solution is None:
        print("   No solution found.")
    else:
        print(f"   Solved in {bt_time:.4f}s")
        print_solution(bt_solution)
        render_map(
            gdf, bt_solution,
            title=(
                "Vietnam – CSP Map Colouring\n"
                "Backtracking + Forward Checking\n"
                "(63 tỉnh/thành phố, trước sát nhập 2025)"
            ),
            output_path="vietnam_csp_map_backtracking.png",
        )

    # ── 2. AC-3 PREPROCESSING + BACKTRACKING + FORWARD CHECKING ─────────
    print("=" * 70)
    print("2) Solving with AC-3 preprocessing + Backtracking + Forward Checking ...")
    t0 = time.perf_counter()
    ac3_solution, reduced_domains = ac3_then_backtracking(province_names, COLORS, neighbors)
    ac3_time = time.perf_counter() - t0

    if reduced_domains is None:
        print("   AC-3 proved the CSP has no solution (a domain became empty).")
    elif ac3_solution is None:
        print("   AC-3 found no contradiction, but backtracking found no solution.")
    else:
        pruned = sum(len(COLORS) - len(d) for d in reduced_domains.values())
        print(f"   AC-3 pruned {pruned} domain value(s) before search began.")
        print(f"   Solved in {ac3_time:.4f}s")
        print_solution(ac3_solution)
        render_map(
            gdf, ac3_solution,
            title=(
                "Vietnam – CSP Map Colouring\n"
                "AC-3 + Backtracking + Forward Checking\n"
                "(63 tỉnh/thành phố, trước sát nhập 2025)"
            ),
            output_path="vietnam_csp_map_ac3_backtracking.png",
        )

    # ── 3. MIN-CONFLICTS (LOCAL SEARCH) ──────────────────────────────────
    print("=" * 70)
    print("3) Solving with Min-Conflicts (local search) ...")
    t0 = time.perf_counter()
    mc_solution = min_conflicts(province_names, COLORS, neighbors, max_steps=10_000, seed=42)
    mc_time = time.perf_counter() - t0

    if mc_solution is None:
        print("   No solution found within max_steps (try increasing max_steps).")
    else:
        print(f"   Solved in {mc_time:.4f}s")
        print_solution(mc_solution)
        render_map(
            gdf, mc_solution,
            title=(
                "Vietnam – CSP Map Colouring\n"
                "Min-Conflicts (Local Search)\n"
                "(63 tỉnh/thành phố, trước sát nhập 2025)"
            ),
            output_path="vietnam_csp_map_min_conflicts.png",
        )

    # ── SUMMARY ───────────────────────────────────────────────────────────
    print("=" * 70)
    print("SUMMARY")
    print(f"   Backtracking + FC        : {bt_time:.4f}s "
          f"{'(' + str(len(set(bt_solution.values()))) + ' colours)' if bt_solution else '(failed)'}")
    print(f"   AC-3 + Backtracking + FC  : {ac3_time:.4f}s "
          f"{'(' + str(len(set(ac3_solution.values()))) + ' colours)' if ac3_solution else '(failed)'}")
    print(f"   Min-Conflicts             : {mc_time:.4f}s "
          f"{'(' + str(len(set(mc_solution.values()))) + ' colours)' if mc_solution else '(failed)'}")


if __name__ == "__main__":
    main()
