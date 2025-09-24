import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from tqdm import tqdm
import cv2

class PhotoRanker:
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
        
        print(f"PhotoRanker initialized. Device: {self.device}")
    
    def _load_model(self):
        """Lazy load the MobileNetV2 model only when needed"""
        if self.model is None:
            print("Loading image quality model...")
            # Use MobileNetV2 from torchvision for image quality assessment
            self.model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
            self.model.eval()
            self.model.to(self.device)
            print("Image quality model loaded successfully!")

    def preprocess_image(self, img):
        """Preprocess image for the model"""
        # Ensure image is in RGB format
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply transforms
        img_tensor = self.transform(img)
        # Add batch dimension
        img_tensor = img_tensor.unsqueeze(0)
        return img_tensor.to(self.device)

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
        """Get quality score for an image using multiple metrics"""
        try:
            # Load model if not already loaded
            self._load_model()
            
            # Get neural network confidence score
            img_tensor = self.preprocess_image(img)
            
            with torch.no_grad():
                predictions = self.model(img_tensor)
                # Apply softmax to get probabilities
                probabilities = F.softmax(predictions, dim=1)
                # Use the highest confidence as one quality metric
                max_confidence = torch.max(probabilities).item()
            
            # Get sharpness score
            sharpness = self.calculate_image_sharpness(img)
            # Normalize sharpness score (typical range 0-2000, normalize to 0-1)
            normalized_sharpness = min(sharpness / 1000.0, 1.0)
            
            # Combine metrics (weighted average)
            # 70% neural network confidence, 30% sharpness
            quality_score = (0.7 * max_confidence + 0.3 * normalized_sharpness) * 10
            
            return quality_score
        except Exception as e:
            print(f"\nError processing image: {str(e)}")
            return 0.0  # Return 0 score for failed images

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