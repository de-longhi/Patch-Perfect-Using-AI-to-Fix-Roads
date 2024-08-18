import os
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.cluster import KMeans
import csv

def read_csv(input_csv):
    """
    Read the CSV file and return a dictionary with filenames and their corresponding k values.
    """
    k_values = {}
    with open(input_csv, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header row
        for row in reader:
            filename, k = row
            k_values[filename] = int(k)
    return k_values

def extract_white_pixel_coordinates(image_path):
    """
    Extract coordinates of white pixels from a black and white image.
    """
    img = Image.open(image_path).convert('L')
    img_array = np.asarray(img)
    white_pixel_coords = np.column_stack(np.where(img_array > 200))  # Adjust threshold if needed
    return white_pixel_coords

def apply_kmeans_to_image(image_path, k):
    """
    Apply K-means clustering to the white pixel coordinates of the image.
    """
    white_pixels = extract_white_pixel_coordinates(image_path)
    if len(white_pixels) == 0:
        return []  # No white pixels, no clusters

    kmeans = KMeans(n_clusters=k, random_state=0).fit(white_pixels)
    return kmeans.cluster_centers_

def write_cluster_centroids(output_csv, centroids_data):
    """
    Write the cluster centroids to a CSV file.
    """
    with open(output_csv, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['image', 'cluster_index', 'centroid_x', 'centroid_y'])
        for image_file, centroids in centroids_data.items():
            for index, centroid in enumerate(centroids):
                writer.writerow([image_file, index] + list(centroid))

def main(input_csv, images_dir, output_csv):
    """
    Main function to read k values, apply K-means clustering, and save the results.
    """
    k_values = read_csv(input_csv)
    centroids_data = {}
    
    for image_file, k in k_values.items():
        image_path = os.path.join(images_dir, image_file)
        centroids = apply_kmeans_to_image(image_path, k)
        centroids_data[image_file] = centroids
    
    write_cluster_centroids(output_csv, centroids_data)
    print("Cluster centroids have been written to", output_csv)

# Define paths for your input CSV, images directory, and output CSV
input_csv = './sorted_output.csv'
images_dir = './data/filtered twice/'
output_csv = 'test_cluster_centroids.csv'

# Execute the main function
main(input_csv, images_dir, output_csv)
