import os
import numpy as np
from PIL import Image

def conway_filter(image, threshold=2):
    """
    Apply a filter similar to Conway's Game of Life.
    If a white pixel doesn't have a certain number of white pixels
    in its 8-neighbor vicinity, it turns black.
    
    Parameters:
        image (PIL.Image): The black and white image.
        threshold (int): Minimum number of white neighbors to keep the pixel white.

    Returns:
        PIL.Image: The filtered black and white image.
    """
    # Convert the image to a NumPy array
    img_array = np.array(image)

    # Create a copy of the image to store the result
    result_array = img_array.copy()

    # Get the dimensions of the image
    rows, cols = img_array.shape

    # Iterate over each pixel (excluding the borders)
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if img_array[i, j] != 0:  # If the pixel is white
                # Check the 8 neighbors
                neighbors = img_array[i-1:i+2, j-1:j+2]
                white_neighbors = np.sum(neighbors != 0) - 1  # Subtract the pixel itself

                # If the number of white neighbors is less than the threshold, turn it black
                if white_neighbors < threshold:
                    result_array[i, j] = 0

    return Image.fromarray(result_array)

def process_images(input_dir, output_dir, threshold=2):
    """
    Process all images in the input directory, apply the Conway-like filter,
    and save the results to the output directory.
    
    Parameters:
        input_dir (str): Path to the directory containing the input images.
        output_dir (str): Path to the directory where the filtered images will be saved.
        threshold (int): Minimum number of white neighbors to keep the pixel white.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Load the image
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path).convert('L')  # Ensure the image is in grayscale

            # Apply the Conway-like filter
            filtered_image = conway_filter(image, threshold)

            # Save the filtered image to the output directory
            output_path = os.path.join(output_dir, filename)
            filtered_image.save(output_path)

            print(f"Processed {filename} and saved filtered image to {output_path}")

# Set your input and output directories
input_directory = './red masks/'
output_directory = './red masks filtered/'

# Process the images with the specified threshold
process_images(input_directory, output_directory, threshold=2)
