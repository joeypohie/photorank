from photo_classifier import PhotoClassifier
from utils import load_images, display_clusters
import os
import tensorflow as tf

def main():
    # Initialize TensorFlow
    print(f"Using TensorFlow version: {tf.__version__}")
    
    # Ask the user for the directory containing photos
    directory = input("Enter the path to your photos directory: ")
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist!")
        return
    
    # Load all images
    print("\nLoading images...")
    images = load_images(directory)
    
    if not images:
        print("No images found in the directory!")
        return
    
    print(f"\nSuccessfully loaded {len(images)} images!")
    
    # Initialize the photo classifier
    classifier = PhotoClassifier()
    
    # Cluster the images
    cluster_groups = classifier.cluster_images(images)
    
    # Display results
    display_clusters(cluster_groups)

if __name__ == "__main__":
    main() 