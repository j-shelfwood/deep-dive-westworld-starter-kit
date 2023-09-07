from PIL import Image, ImageDraw, ImageFont
import os
from tqdm import tqdm
import shutil

# Load the map image
image_path = "../images/map.png"
image = Image.open(image_path)

# Path to save the tiles
tiles_path = "../tiles/"

# Clear previous tiles directory and create a new one
shutil.rmtree(tiles_path, ignore_errors=True)
os.makedirs(tiles_path, exist_ok=True)

# Function to generate tiles for a given zoom level and grid size
def generate_tiles(image, zoom_level, grid_size):
    dynamic_tile_size = max(image.width, image.height) // grid_size
    resized_image = image.resize(
        (dynamic_tile_size * grid_size, dynamic_tile_size * grid_size), Image.BILINEAR
    )

    # Create tiles
    for x in tqdm(range(grid_size + 1), desc=f"Generating tiles for zoom level {zoom_level}"):
        for y in range(grid_size + 1):
            left = x * dynamic_tile_size
            upper = y * dynamic_tile_size
            right = left + dynamic_tile_size
            lower = upper + dynamic_tile_size

            tile = resized_image.crop((left, upper, right, lower))

            tile_path = os.path.join(tiles_path, str(zoom_level))
            os.makedirs(tile_path, exist_ok=True)
            tile.save(os.path.join(tile_path, f"{x}-{grid_size - y}.png"))

# Manually specify grid sizes for each zoom level
zoom_level_grid_sizes = {
    -1: 4,
    0: 8,
    1: 16,
}

# Generate tiles for specified zoom levels
for zoom_level, grid_size in zoom_level_grid_sizes.items():
    generate_tiles(image, zoom_level, grid_size)
