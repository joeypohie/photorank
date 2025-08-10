import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from sklearn.cluster import DBSCAN
from tqdm import tqdm
from photo_ranker import PhotoRanker
from PIL import Image

class PhotoClassifier:
    def __init__(self):
        print("Loading ResNet50 model...")
        # Load pre-trained ResNet50 model
        self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        # Remove the final classification layer to get features
        self.model = nn.Sequential(*list(self.model.children())[:-1])
        self.model.eval()  # Set to evaluation mode
        print("ResNet50 model loaded successfully!")
        
        # Set device (CPU or GPU)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        print(f"Using device: {self.device}")
        
        # Define image preprocessing transforms
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Initialize photo ranker
        self.ranker = PhotoRanker()

    def preprocess_image(self, img):
        """Preprocess image for ResNet"""
        # Ensure image is in RGB format
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply transforms
        img_tensor = self.transform(img)
        # Add batch dimension
        img_tensor = img_tensor.unsqueeze(0)
        return img_tensor.to(self.device)

    def extract_features(self, img):
        """Extract features using ResNet"""
        try:
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