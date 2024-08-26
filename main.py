import os
import configparser
import logging
from PIL import Image
import math
import sys  # Add this import to allow exiting with a specific code

# Set up logging to log.txt
logging.basicConfig(filename='log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Logging has started.")

def parse_size(size_str):
    """Helper function to parse size strings like '8x8' or '64x64'."""
    return tuple(map(int, size_str.lower().split('x')))

def create_subuv_texture(folder_path, output_path, grid_size, tile_size):
    logging.info(f"Starting SubUV texture creation. Input folder: {folder_path}, Output file: {output_path}")

    # Load images from the folder
    images = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(img_path)
                images.append(img)
                logging.info(f"Loaded image: {filename}")
            except Exception as e:
                logging.error(f"Failed to load image {filename}: {e}")
                print(f"Error: Failed to load image {filename}: {e}")
                return 1

    if not images:
        logging.error("No images were loaded. Please check the input folder.")
        print("Error: No images were loaded. Please check the input folder.")
        return 1

    # Determine the total size of the grid based on grid size and tile size
    grid_columns, grid_rows = grid_size
    grid_width = grid_columns * tile_size[0]
    grid_height = grid_rows * tile_size[1]
    logging.info(f"Grid size: {grid_columns}x{grid_rows}, Total grid dimensions: {grid_width}x{grid_height}")

    # Create a new image with the calculated grid size
    grid_image = Image.new('RGBA', (grid_width, grid_height))
    logging.info(f"Created a blank grid image of size {grid_width}x{grid_height}")

    # Paste images into the grid
    for index, img in enumerate(images):
        if index >= grid_columns * grid_rows:
            logging.warning(f"More images than grid slots. Skipping image {index}")
            break

        # Resize the image to fit the tile size
        img_resized = img.resize(tile_size)
        logging.info(f"Resized image {index} to {tile_size}")
        
        x = (index % grid_columns) * tile_size[0]
        y = (index // grid_columns) * tile_size[1]
        grid_image.paste(img_resized, (x, y))
        logging.info(f"Pasted image {index} at position ({x}, {y})")

    # Save the grid image as the final SubUV texture
    try:
        grid_image.save(output_path)
        logging.info(f"Successfully saved the SubUV texture to {output_path}")
        print(f"Successfully saved the SubUV texture to {output_path}")
        return 0  # Success
    except Exception as e:
        logging.error(f"Failed to save the SubUV texture: {e}")
        print(f"Error: Failed to save the SubUV texture: {e}")
        return 1  # Failure

# Load settings from the ini file
config = configparser.ConfigParser()
config.read('settings.ini')

# Read paths from the settings file
folder_path = config['Paths']['input_folder']
output_path = config['Paths']['output_file']

# Read grid settings
grid_size = parse_size(config['GridSettings']['image_size'])
tile_size = parse_size(config['GridSettings']['tile_size'])

# Create the SubUV texture
exit_code = create_subuv_texture(folder_path, output_path, grid_size, tile_size)
sys.exit(exit_code)  # Exit with the appropriate code
