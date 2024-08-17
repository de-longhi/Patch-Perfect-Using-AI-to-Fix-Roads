import os
import pandas as pd
from PIL import Image, ImageDraw

def read_centroids_from_csv(csv_file):
    """
    Read centroids from the CSV file and store them in a dictionary.
    """
    centroids = {}
    df = pd.read_csv(csv_file)
    
    for _, row in df.iterrows():
        image_file = row['image']
        centroid_x = row['centroid_x']
        centroid_y = row['centroid_y']
        cluster_index = row['cluster_index']
        
        if image_file not in centroids:
            centroids[image_file] = []
        
        centroids[image_file].append((centroid_x, centroid_y, cluster_index))
    
    return centroids

def draw_centroids_on_image(image_path, centroids, output_path):
    """
    Draw circles at the centroid locations on the image.
    """
    img = Image.open(image_path).convert('RGB')
    draw = ImageDraw.Draw(img)
    radius = 5  # Radius of the circle

    for (y, x, _) in centroids:
        # Draw a circle at the centroid location
        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], outline='cyan', width=3)
    
    img.save(output_path)

def main(csv_file, images_dir, output_dir):
    """
    Main function to process the centroids and draw them on the images.
    """
    centroids = read_centroids_from_csv(csv_file)
    os.makedirs(output_dir, exist_ok=True)
    
    for image_file, coords in centroids.items():
        image_path = os.path.join(images_dir, image_file[5:])
        output_path = os.path.join(output_dir, image_file)
        
        if os.path.exists(image_path):
            draw_centroids_on_image(image_path, coords, output_path)
            print(f"Circles drawn and saved to {output_path}")
        else:
            print(f"Image {image_path} does not exist.")

# Define paths for your input CSV, images directory, and output directory
csv_file = 'cluster_centroids.csv'
images_dir = './data/stick subset/'
output_dir = './images_with_centroids'

# Execute the main function
main(csv_file, images_dir, output_dir)
