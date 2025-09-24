import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from sklearn.cluster import DBSCAN
from tqdm import tqdm
from PIL import Image
import cv2

class PhotoClassifierLite:
    """
    Memory-optimized version for Hobby plan (512MB limit)
    Uses MobileNetV2 for both feature extraction and quality assessment
    """
    def __init__(self):
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Define image preprocessing transforms
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        print(f"PhotoClassifierLite initialized. Device: {self.device}")
    
    def _load_model(self):
        """Lazy load the MobileNetV2 model only when needed"""
        if self.model is None:
            print("Loading MobileNetV2 model (lite version)...")
            # Use MobileNetV2 for both feature extraction and quality assessment
            self.model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
            # Remove the final classification layer to get features
            self.model = nn.Sequential(*list(self.model.children())[:-1])
            self.model.eval()
            self.model.to(self.device)
            print("MobileNetV2 model loaded successfully!")
    
    def preprocess_image(self, img):
        """Preprocess image for MobileNetV2"""
        # Ensure image is in RGB format
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply transforms
        img_tensor = self.transform(img)
        # Add batch dimension
        img_tensor = img_tensor.unsqueeze(0)
        return img_tensor.to(self.device)

    def extract_features(self, img):
        """Extract features using MobileNetV2"""
        try:
            # Load model if not already loaded
            self._load_model()
            
            img_tensor = self.preprocess_image(img)
            
            with torch.no_grad():
                features = self.model(img_tensor)
                # Flatten the features
                features = features.view(features.size(0), -1)
                # Convert to numpy array
                features = features.cpu().numpy().flatten()
            
            return features
        except Exception as e:
            print(f"\nError extracting features: {str(e)}")
            return None

    def calculate_image_sharpness(self, img):
        """Calculate image sharpness using Laplacian variance"""
        try:
            # Convert PIL image to OpenCV format
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            # Convert to grayscale
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            # Calculate Laplacian variance (measure of sharpness)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            return laplacian_var
        except Exception as e:
            print(f"Error calculating sharpness: {str(e)}")
            return 0.0

    def get_quality_score(self, img):
        """Get quality score using sharpness only (no neural network)"""
        try:
            # Get sharpness score
            sharpness = self.calculate_image_sharpness(img)
            # Normalize sharpness score (typical range 0-2000, normalize to 0-1)
            normalized_sharpness = min(sharpness / 1000.0, 1.0)
            
            # Use sharpness as quality score (multiply by 10 for consistency)
            quality_score = normalized_sharpness * 10
            
            return quality_score
        except Exception as e:
            print(f"\nError processing image: {str(e)}")
            return 0.0

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
        return self.rank_clusters(cluster_groups)

    def rank_images_in_cluster(self, images):
        """Rank images in a cluster based on quality scores"""
        ranked_images = []
        for filename, img in images:
            try:
                score = self.get_quality_score(img)
                ranked_images.append((filename, score))
            except Exception as e:
                print(f"\nError scoring {filename}: {str(e)}")
        
        # Sort by score in descending order
        ranked_images.sort(key=lambda x: x[1], reverse=True)
        return ranked_images

    def rank_clusters(self, cluster_groups):
        """Rank images within each cluster"""
        ranked_clusters = {}
        print("\nRanking images within clusters...")
        for cluster_id, cluster_images in tqdm(cluster_groups.items(), desc="Ranking clusters"):
            ranked_images = self.rank_images_in_cluster(cluster_images)
            ranked_clusters[cluster_id] = ranked_images
        
        return ranked_clusters
