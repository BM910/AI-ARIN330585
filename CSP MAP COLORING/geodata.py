import json
import os
from shapely.geometry import shape

def load_map_data(geojson_path):
    """
    Reads a geojson file and returns:
    1. A list of all province names (variables)
    2. A dictionary mapping each province to a list of its neighbors (constraints)
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(geojson_path):
        geojson_path = os.path.join(base_dir, geojson_path)

    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    variables = []
    geometries = {}

    # 1. First pass: Extract names and shapes from the GeoJSON
    for feature in data['features']:
        name = feature['properties']['ten_tinh']
        variables.append(name)
        # Convert the raw coordinates into a geometry object we can check borders with
        geometries[name] = shape(feature['geometry'])

    # 2. Second pass: Compare every province to find its neighbors
    neighbors = {v: [] for v in variables}
    
    for p1 in variables:
        for p2 in variables:
            if p1 != p2:
                # .intersects() checks if they share a border or touch
                if geometries[p1].intersects(geometries[p2]):
                    neighbors[p1].append(p2)

    return variables, neighbors

# test
if __name__ == "__main__":
    provinces, adj_map = load_map_data("borders.geojson")
    print(f"Loaded {len(provinces)} provinces.")
    print(f"Neighbors for An Giang: {adj_map.get('An Giang')}")