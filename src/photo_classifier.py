import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.cluster import DBSCAN
from tqdm import tqdm
from photo_ranker import PhotoRanker

class PhotoClassifier:
    def __init__(self):
        print("Loading ResNet50 model...")
        # Load ResNet50 model without the top classification layer
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        print("ResNet50 model loaded successfully!")
        
        # Initialize photo ranker
        self.ranker = PhotoRanker()

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
        try:
            img_array = self.preprocess_image(img)
            features = self.model.predict(img_array, verbose=0)
            return features.flatten()
        except Exception as e:
            print(f"\nError extracting features: {str(e)}")
            return None

    def cluster_images(self, images, eps=0.3, min_samples=2):
        """Cluster similar images using DBSCAN"""
        print("\nExtracting features from images...")
        features = []
        filenames = []
        image_dict = {}  # Store images for later ranking
        
        # Create progress bar for feature extraction
        for filename, img in tqdm(images, desc="Extracting features"):
            try:
                feature = self.extract_features(img)
                if feature is not None:
                    features.append(feature)
                    filenames.append(filename)
                    image_dict[filename] = img
            except Exception as e:
                print(f"\nError processing {filename}: {str(e)}")
        
        if not features:
            print("No features extracted from images!")
            return {}
        
        features = np.array(features)
        print(f"\nExtracted features from {len(features)} images")
        print("\nClustering images...")
        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
        clusters = clustering.fit_predict(features)
        
        # Group images by cluster
        cluster_groups = {}
        for idx, cluster_id in enumerate(clusters):
            if cluster_id not in cluster_groups:
                cluster_groups[cluster_id] = []
            cluster_groups[cluster_id].append((filenames[idx], image_dict[filenames[idx]]))
        
        print(f"Found {len(cluster_groups)} clusters")
        # Rank images within each cluster
        return self.ranker.rank_clusters(cluster_groups) 