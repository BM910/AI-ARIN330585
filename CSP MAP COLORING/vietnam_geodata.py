"""
vietnam_geodata.py

Provides geographic data for Vietnam's 63 provinces pre-2025
loaded from a local GeoJSON file.

The GeoJSON uses the following properties per feature:
  - ten_tinh : official Vietnamese province name
  - ma_tinh  : province code
  - loai     : type (Tỉnh / Thành phố trực thuộc TW)

Exports
-------
load_vietnam_geodata(geojson_path) -> tuple[GeoDataFrame, dict[str, set[str]]]
    Returns (gdf, neighbors) where:
      - gdf       : GeoDataFrame with columns ["name", "geometry"], 63 rows
      - neighbors : adjacency dict {province_name: set_of_neighbor_names}
"""

import warnings
warnings.filterwarnings("ignore")

import geopandas as gpd
from collections import defaultdict

# ──────────────────────────────────────────────────────────────────────────────
# DEFAULT PATH — update if your file lives elsewhere
# ──────────────────────────────────────────────────────────────────────────────
DEFAULT_GEOJSON_PATH = "borders.geojson"


def _load_gdf(geojson_path: str) -> gpd.GeoDataFrame:
    """Read the GeoJSON and return a clean GeoDataFrame."""
    print(f"Loading geodata from '{geojson_path}' ...")
    gdf = gpd.read_file(geojson_path)
    # Rename ten_tinh → name for consistent downstream use
    gdf = gdf.rename(columns={"ten_tinh": "name"})[["name", "geometry"]].copy()
    gdf = gdf.set_crs("EPSG:4326", allow_override=True)
    print(f"   → {len(gdf)} provinces loaded.")
    return gdf


def _build_adjacency(gdf: gpd.GeoDataFrame) -> dict[str, set[str]]:
    """
    Return a dict mapping each province name to the set of its neighbours.
    Two provinces are neighbours when their geometries touch or share a
    non-empty border (determined via Shapely predicates).
    """
    print("Building adjacency graph ...")
    names = list(gdf["name"])
    n = len(names)
    neighbors: dict[str, set[str]] = defaultdict(set)

    for i in range(n):
        for j in range(i + 1, n):
            gi = gdf.geometry.iloc[i]
            gj = gdf.geometry.iloc[j]
            if gi is None or gj is None:
                continue
            try:
                if gi.touches(gj) or (
                    gi.intersects(gj) and not gi.intersection(gj).is_empty
                ):
                    neighbors[names[i]].add(names[j])
                    neighbors[names[j]].add(names[i])
            except Exception:
                pass

    edge_count = sum(len(v) for v in neighbors.values()) // 2
    print(f"   → {edge_count} adjacency edges found.")
    return dict(neighbors)


def load_vietnam_geodata(
    geojson_path: str = DEFAULT_GEOJSON_PATH,
) -> tuple[gpd.GeoDataFrame, dict[str, set[str]]]:
    """
    Load geodata and compute adjacency from a local GeoJSON file.

    Parameters
    ----------
    geojson_path : str
        Path to the borders.geojson file.

    Returns
    -------
    gdf       : GeoDataFrame  columns=["name", "geometry"],  63 rows
    neighbors : dict[str, set[str]]  province → set of adjacent provinces
    """
    gdf = _load_gdf(geojson_path)
    neighbors = _build_adjacency(gdf)
    print()
    return gdf, neighbors
