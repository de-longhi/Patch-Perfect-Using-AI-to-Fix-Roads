import os
from PIL import Image
import numpy as np

def create_mask(image, color_range):
    # Convert the image to a NumPy array
    np_img = np.array(image)
    
    # Create a mask with the same size as the image, initialized to black (0)
    mask = np.zeros((np_img.shape[0], np_img.shape[1]), dtype=np.uint8)

    # Define the color range
    r_min, r_max = color_range[0]
    g_min, g_max = color_range[1]
    b_min, b_max = color_range[2]

    # Apply the mask where the RGB values fall within the specified range
    within_range = (
        (np_img[:, :, 0] >= r_min) & (np_img[:, :, 0] <= r_max) &  # Red channel
        (np_img[:, :, 1] >= g_min) & (np_img[:, :, 1] <= g_max) &  # Green channel
        (np_img[:, :, 2] >= b_min) & (np_img[:, :, 2] <= b_max)    # Blue channel
    )

    # Set the mask pixels to white (255) where the condition is met
    mask[within_range] = 255

    return Image.fromarray(mask)

def process_images(input_dir, output_dir, color_range):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Load the image
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path)

            # Create the mask
            mask = create_mask(image, color_range)

            # Save the mask to the output directory
            mask_filename = f"mask_{filename}"
            mask.save(os.path.join(output_dir, mask_filename))

            print(f"Processed {filename} and saved mask as {mask_filename}")

# Define the color range [R_min, R_max, G_min, G_max, B_min, B_max]
color_range = [(215, 255), (70, 135), (70, 120)]

# Set your input and output directories
input_directory = './test set/'
output_directory = './test red masks/'

# Process the images
process_images(input_directory, output_directory, color_range)
