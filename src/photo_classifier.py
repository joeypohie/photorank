import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.cluster import DBSCAN
from tqdm import tqdm

class PhotoClassifier:
    def __init__(self):
        print("Loading ResNet50 model...")
        # Load ResNet50 model without the top classification layer
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        print("ResNet50 model loaded successfully!")

    def preprocess_image(self, img):
        """Preprocess image for ResNet"""
        # Resize image to 224x224 (required by ResNet)
        img = img.resize((224, 224))
        # Convert to numpy array
        img_array = np.array(img)
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        # Preprocess for ResNet
        img_array = preprocess_input(img_array)
        return img_array

    def extract_features(self, img):
        """Extract features using ResNet"""
        img_array = self.preprocess_image(img)
        features = self.model.predict(img_array, verbose=0)  # Suppress TensorFlow progress
        return features.flatten()

    def cluster_images(self, images, eps=0.3, min_samples=2):
        """Cluster similar images using DBSCAN"""
        print("\nExtracting features from images...")
        features = []
        filenames = []
        
        # Create progress bar for feature extraction
        for filename, img in tqdm(images, desc="Extracting features"):
            try:
                feature = self.extract_features(img)
                features.append(feature)
                filenames.append(filename)
            except Exception as e:
                print(f"\nError processing {filename}: {str(e)}")
        
        if not features:
            return []
        
        features = np.array(features)
        print("\nClustering images...")
        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
        clusters = clustering.fit_predict(features)
        
        # Group images by cluster
        cluster_groups = {}
        for idx, cluster_id in enumerate(clusters):
            if cluster_id not in cluster_groups:
                cluster_groups[cluster_id] = []
            cluster_groups[cluster_id].append(filenames[idx])
        
        return cluster_groups 