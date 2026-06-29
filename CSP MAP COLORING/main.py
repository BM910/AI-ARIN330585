from geodata import load_map_data
from solvers import backtrack, forwardcheck, min_conflicts, backtrack_ac3
from visualizer import save_map_image

import os
import time
import geopandas as gpd

RED = "#E63946"
GREEN = "#2A9D8F"
YELLOW = "#E9C46A"
BLUE = "#457B9D"

script_dir = os.path.dirname(os.path.abspath(__file__))
geojson_path = os.path.join(script_dir, "borders.geojson")

# Load variables and constraints
print("Loading map data...")
variables, neighbors = load_map_data(geojson_path)

# Setup domain colors
colors = [RED, GREEN, YELLOW, BLUE]
print(f"Domain colors: {colors}")
domains = {v: colors.copy() for v in variables}

# Load data frame
print("Reading map...")
gdf = gpd.read_file(geojson_path)
print()


# ===== BACKTRACK =====
start_time = time.perf_counter()
backtrack_solution = backtrack(variables, domains, {}, neighbors)
end_time = time.perf_counter()
print(f"Backtracking finished in {end_time - start_time:.4f} seconds.")

if backtrack_solution:
    out_img = os.path.join(script_dir, "vn_csp_coloring_backtracking.png")
    save_map_image(gdf,
                   solution=backtrack_solution, 
                   title=f"Vietnam Map CSP Coloring\nBacktracking {(end_time - start_time) * 1000:.1f}ms", 
                   output_filename=out_img
                   )
print()
# =====================


# ===== FORWARD CHECK =====
start_time = time.perf_counter()
backtrack_fc_solution = forwardcheck(variables, domains, {}, neighbors)
end_time = time.perf_counter()
print(f"Forward Checking finished in {end_time - start_time:.4f} seconds.")

if backtrack_fc_solution:
    out_img = os.path.join(script_dir, "vn_csp_coloring_forward_checking.png")
    save_map_image(gdf,
                   solution=backtrack_fc_solution, 
                   title=f"Vietnam Map CSP Coloring\nForward Checking {(end_time - start_time) * 1000:.1f}ms", 
                   output_filename=out_img
                   )
print()
# =====================================


# ===== BACKTRACK + AC3 =====
hard_locked_domains = domains.copy()
hard_locked_provinces = {
    "Bình Phước" : [BLUE], 
    "Bình Thuận" : [BLUE], 
    "Khánh Hòa" : [BLUE], 
    "Hà Nội": [BLUE],
    "Gia Lai" : [YELLOW],
    "Quảng Nam" : [YELLOW],
    "Quảng Trị" : [YELLOW]
}
hard_locked_domains.update(hard_locked_provinces)

start_time = time.perf_counter()
backtrack_ac3_solution = backtrack_ac3(variables, hard_locked_domains, {}, neighbors)
end_time = time.perf_counter()
print(f"Backtracking + AC-3 finished in {end_time - start_time:.4f} seconds.")

if backtrack_ac3_solution:
    out_img = os.path.join(script_dir, "vn_csp_coloring_backtracking_ac3.png")
    save_map_image(gdf,
                   solution=backtrack_ac3_solution, 
                   title=f"Vietnam Map CSP Coloring\nBacktracking and AC-3 {(end_time - start_time) * 1000:.1f}ms", 
                   output_filename=out_img
                   )
print()
# ===========================


# ===== MIN-CONFLICTS =====
min_conflicts_solution = None
attempts = 0

start_time = time.perf_counter()
while min_conflicts_solution is None and attempts < 5:
    attempts += 1
    min_conflicts_solution = min_conflicts(variables, domains, neighbors, max_steps=100)
end_time = time.perf_counter()
print(f"Min-Conflicts finished in {end_time - start_time:.4f} seconds (Attempts: {attempts}).")

if min_conflicts_solution:
    out_img = os.path.join(script_dir, "vn_csp_coloring_min_conflicts.png")
    save_map_image(gdf,
                   solution=min_conflicts_solution, 
                   title=f"Vietnam Map CSP Coloring\nMin-Conflicts {(end_time - start_time) * 1000:.1f}ms {attempts} attempt(s)", 
                   output_filename=out_img
                   )
# =========================