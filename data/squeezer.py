import os
from PIL import Image
import torch
from torchvision import transforms
from pathlib import Path

def resize_images(input_dir, output_dir, size=(128, 128)):
    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Define the transform to resize images
    transform = transforms.Compose([
        transforms.Resize(size),
    ])

    # Loop over all files in the input directory
    for image_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, image_name)
        
        # Check if the file is an image
        try:
            with Image.open(input_path) as img:
                # Apply the transformation
                img_resized = transform(img)
                
                # Save the resized image to the output directory
                output_path = os.path.join(output_dir, image_name)
                img_resized.save(output_path)
                
                print(f"Saved resized image to {output_path}")
        except IOError:
            print(f"File {input_path} is not a valid image file and will be skipped.")

if __name__ == "__main__":
    # Example usage:
    input_directory = "./train_images_segmented/"
    output_directory = "./stick subset/"
    target_size = (448, 448)  # Resize images to 256x256

    resize_images(input_directory, output_directory, size=target_size)
