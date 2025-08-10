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
    """Display clustering and ranking results"""
    if not cluster_groups:
        print("\nNo clusters found. This might mean:")
        print("1. No similar images were found")
        print("2. The clustering parameters might need adjustment")
        return
        
    print("\nClustering and Ranking Results:")
    
    # First, handle unclustered images (cluster_id = -1)
    if -1 in cluster_groups:
        print("\nUnclustered images (no similar matches found):")
        for filename, score in cluster_groups[-1]:
            print(f"- {filename} (Score: {score:.2f})")
    
    # Then handle the clusters
    for cluster_id, ranked_images in cluster_groups.items():
        if cluster_id == -1:  # Skip unclustered images as we handled them above
            continue
        if not ranked_images:  # Skip empty clusters
            continue
            
        print(f"\nCluster {cluster_id} (similar images, ranked by quality):")
        print(f"Number of images in cluster: {len(ranked_images)}")
        for filename, score in ranked_images:
            print(f"- {filename} (Score: {score:.2f})")
        
        # Only show recommendation if there are ranked images
        if ranked_images:
            print(f"  Recommended to keep: {ranked_images[0][0]} (Score: {ranked_images[0][1]:.2f})")
        else:
            print("  No images in this cluster to recommend") 