import matplotlib.pyplot as plt

def save_map_image(gdf, solution, title="Vietnam Map Coloring CSP Solution", output_filename="map_solution.png", bg_color="#1a1a2e"):
    gdf_copy = gdf.copy()
    gdf_copy['color'] = gdf_copy['ten_tinh'].map(solution).fillna('lightgrey')
    
    fig, ax = plt.subplots(figsize=(10, 12), facecolor=bg_color)
    ax.set_facecolor(bg_color)

    gdf_copy.plot(ax=ax, color=gdf_copy['color'], edgecolor="#ffffff", linewidth=0.5)
    
    for idx, row in gdf_copy.iterrows():
        centroid = row['geometry'].centroid
        
        ax.text(
            centroid.x,
            centroid.y,
            s=row['ten_tinh'],
            fontsize=3,
            color="white",
            ha="center",
            va="center",
            weight="bold",
            alpha=0.85,
            bbox=dict(boxstyle="round,pad=0.15", fc=(0, 0, 0, 0.38), lw=0)
        )

    ax.set_axis_off()
    plt.title(title, fontsize=16, pad=20, color="white")
    
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    print(f"Map successfully saved as '{output_filename}'!")

# test
if __name__ == "__main__":
    mock_solution = {
        "An Giang": "#E63946",
        "Cần Thơ": "#2A9D8F",
        "Kiên Giang": "#E9C46A",
        "Đồng Tháp": "#457B9D"
    }
    save_map_image("borders.geojson", mock_solution, "test_map.png")