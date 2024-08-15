import os
import json
import cv2
import numpy as np

def create_binary_mask(annotation_file, output_dir):
    # Load the annotation JSON file
    with open(annotation_file, 'r') as f:
        data = json.load(f)

    # Get image dimensions
    image_height = data['imageHeight']
    image_width = data['imageWidth']

    # Create a black image (binary mask)
    mask = np.zeros((image_height, image_width), dtype=np.uint8)

    # Loop through each shape in the annotation file
    for shape in data['shapes']:
        if shape['shape_type'] == 'polygon':
            color = 255 if shape['label'] == 'pothole'  else 100
            # Extract the points for the polygon
            points = np.array(shape['points'], dtype=np.int32)
            # Fill the polygon in the mask with white color (255)
            cv2.fillPoly(mask, [points], color=color)

    # Get the filename and save the mask
    image_filename = os.path.basename(data['imagePath'])
    mask_filename = os.path.splitext(image_filename)[0] + '_mask.png'
    mask_output_path = os.path.join(output_dir, mask_filename)

    cv2.imwrite(mask_output_path, mask)

def process_directory(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each annotation file in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            annotation_file = os.path.join(input_dir, filename)
            create_binary_mask(annotation_file, output_dir)

if __name__ == "__main__":
    # Specify the directory containing the annotation files
    input_dir = './temp_02/'
    # Specify the directory where the binary masks will be saved
    output_dir = './masks/'

    # Process the directory
    process_directory(input_dir, output_dir)
