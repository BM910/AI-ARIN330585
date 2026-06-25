from geodata import load_map_data
from solvers import backtrack_fc, min_conflicts, backtrack_ac3, ac3
from visualizer import save_map_image

import time
import geopandas as gpd

# Load variables and constraints
print("Loading map data...")
variables, neighbors = load_map_data("borders.geojson")

# Setup domain colors
colors = ["#E63946", "#2A9D8F", "#E9C46A", "#457B9D"]
domains = {v: colors.copy() for v in variables}

# Run solvers
print("Running algorithms...")


start_time = time.perf_counter()
backtrack_fc_solution = backtrack_fc(variables, domains, {}, neighbors)
end_time = time.perf_counter()
print(f"Backtracking + Forward Checking finished in {end_time - start_time:.4f} seconds.")


hard_locked_domains = domains.copy()
hard_locked_provinces = {
    "Bình Phước" : ["#457B9D"], 
    "Bình Thuận" : ["#457B9D"], 
    "Khánh Hòa" : ["#457B9D"], 
    "Hà Nội": ["#457B9D"],
    "Gia Lai" : ["#E9C46A"],
    "Quảng Nam" : ["#E9C46A"],
    "Quảng Trị" : ["#E9C46A"]
}
hard_locked_domains.update(hard_locked_provinces)
print(f"Hard locked provinces: {hard_locked_provinces}")
start_time = time.perf_counter()
backtrack_ac3_solution = backtrack_ac3(variables, hard_locked_domains, {}, neighbors)
end_time = time.perf_counter()
print(f"Backtracking + AC-3 finished in {end_time - start_time:.4f} seconds.")


start_time = time.perf_counter()
min_conflicts_solution = None
attempts = 0

while min_conflicts_solution is None and attempts < 5:
    attempts += 1
    min_conflicts_solution = min_conflicts(variables, domains, neighbors, max_steps=100)

end_time = time.perf_counter()
print(f"Min-Conflicts finished in {end_time - start_time:.4f} seconds (Attempts: {attempts}).")


# Load data frame
print("Reading map...")
gdf = gpd.read_file("borders.geojson")

# Save image
if backtrack_fc_solution:
    save_map_image(gdf,
                   solution=backtrack_fc_solution, 
                   title="Vietnam Map CSP Coloring\nBacktracking and Forward Checking", 
                   output_filename="vn_csp_coloring_backtracking_fc.png"
                   )
if backtrack_ac3_solution:
    save_map_image(gdf,
                   solution=backtrack_ac3_solution, 
                   title="Vietnam Map CSP Coloring\nBacktracking and AC-3", 
                   output_filename="vn_csp_coloring_backtracking_ac3.png"
                   )
if min_conflicts_solution:
    save_map_image(gdf,
                   solution=min_conflicts_solution, 
                   title="Vietnam Map CSP Coloring\nMin-Conflicts", 
                   output_filename="vn_csp_coloring_min_conflicts.png"
                   )