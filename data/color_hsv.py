import cv2
import os
from PIL import Image
import numpy as np

def create_hsv_mask(image, hsv_ranges):
    # Convert the image to HSV color space using OpenCV
    hsv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)

    # Create the mask based on the HSV range
    #mask = cv2.inRange(hsv_img, hsv_range[0], hsv_range[1])
    mask = np.zeros(hsv_img.shape[:2], dtype=np.uint8)
    # for hsv_range in hsv_ranges:
    #     mask |= cv2.inRange(hsv_img, hsv_range[0], hsv_range[1])
    
    for hsv_range in hsv_ranges:
        temp_mask = cv2.inRange(hsv_img, hsv_range[0], hsv_range[1])
        
        mask = cv2.bitwise_or(mask, temp_mask)
    return Image.fromarray(mask)


def process_images_hsv(input_dir, output_dir, hsv_ranges):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Load the image
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path)

            # Create the mask using HSV
            mask = create_hsv_mask(image, hsv_ranges)

            # Save the mask to the output directory
            mask_filename = f"mask_{filename}"
            mask.save(os.path.join(output_dir, mask_filename))

            print(f"Processed {filename} and saved mask as {mask_filename}")

# Define the HSV range for the red color (you may need to adjust these values)
hsv_ranges = [
    (np.array([0, 85, 90]), np.array([5, 255, 255])),  # Bright red
    (np.array([170, 85, 100]), np.array([179, 255, 255]))  # Darker red
    # (np.array([0, 100, 20]), np.array([8, 255, 255])),  # Bright red
    # (np.array([160, 100, 20]), np.array([179, 255, 255]))  # Darker red
]  # Example for red

# Set your input and output directories
input_directory = './test set resized/'
output_directory = './test red masks/'

# Process the images using HSV masking
process_images_hsv(input_directory, output_directory, hsv_ranges)
