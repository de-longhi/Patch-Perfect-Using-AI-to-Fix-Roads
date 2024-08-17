import os
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.cluster import DBSCAN

def extract_white_pixel_coords(image):
    """
    Extracts the coordinates of white pixels from a black and white image.
    
    Parameters:
        image (PIL.Image): The black and white image.
        
    Returns:
        np.ndarray: Coordinates of white pixels.
    """
    img_array = np.asarray(image)
    white_pixel_coords = np.column_stack(np.where(img_array == 255))
    return white_pixel_coords

def find_clusters_with_dbscan(pixel_coords, eps=5):
    """
    Finds clusters of white pixels using DBSCAN clustering algorithm.
    
    Parameters:
        pixel_coords (np.ndarray): Coordinates of white pixels.
        eps (float): Maximum distance between two samples for them to be considered as in the same neighborhood.
        
    Returns:
        int: Number of clusters found.
    """
    if pixel_coords.shape[0] == 0:
        return 0  # No white pixels, so no clusters
    
    # Apply DBSCAN clustering
    dbscan = DBSCAN(eps=eps, min_samples=1, metric='euclidean')
    labels = dbscan.fit_predict(pixel_coords)
    
    # Number of unique clusters
    num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    
    return num_clusters

def process_images(input_dir, eps):
    """
    Processes all images in the input directory to find the number of distinct 
    clusters of white pixels using DBSCAN.
    
    Parameters:
        input_dir (str): Path to the directory containing the black and white images.
        eps (float): Maximum distance between two samples for DBSCAN.
        
    Returns:
        pd.DataFrame: A DataFrame containing the image filenames and the number of clusters.
    """
    results = []
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path).convert('L')  # Ensure the image is in grayscale
            
            pixel_coords = extract_white_pixel_coords(image)
            
            # Find clusters using DBSCAN
            num_clusters = find_clusters_with_dbscan(pixel_coords, eps)
            
            results.append({
                'image': filename,
                'num_classes': num_clusters
            })
    
    return pd.DataFrame(results)

def save_results_to_csv(results_df, output_csv):
    """
    Saves the results to a CSV file.
    
    Parameters:
        results_df (pd.DataFrame): DataFrame containing the image filenames and the number of clusters.
        output_csv (str): Path to the output CSV file.
    """
    results_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

# Set the input directory and output CSV file path
input_directory = './data/red masks filtered/'
output_csv = './image_classes.csv'

# Distance parameter for DBSCAN
distance_param = 30

# Process the images and save results
results_df = process_images(input_directory, distance_param)
save_results_to_csv(results_df, output_csv)
