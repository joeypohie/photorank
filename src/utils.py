import os
from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm

# Register HEIF opener
register_heif_opener()

def load_images(directory):
    """Load all images from a directory"""
    images = []
    # Get list of image files first
    image_files = [f for f in os.listdir(directory) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.heic'))]
    
    print("\nLoading images...")
    for filename in tqdm(image_files, desc="Loading images"):
        try:
            image_path = os.path.join(directory, filename)
            img = Image.open(image_path)
            images.append((filename, img))
        except Exception as e:
            print(f"\nCould not load {filename}: {str(e)}")
    return images

def display_clusters(cluster_groups):
    """Display clustering results"""
    print("\nClustering Results:")
    for cluster_id, filenames in cluster_groups.items():
        if cluster_id == -1:
            print("\nUnclustered images (no similar matches found):")
        else:
            print(f"\nCluster {cluster_id + 1} (similar images):")
        for filename in filenames:
            print(f"- {filename}") 