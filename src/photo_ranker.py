import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.applications.resnet50 import preprocess_input
from tqdm import tqdm

class PhotoRanker:
    def __init__(self):
        print("Loading image quality model...")
        # Load the model from TensorFlow Hub
        self.model = hub.load('https://tfhub.dev/google/imagenet/mobilenet_v2_130_224/classification/4')
        print("Image quality model loaded successfully!")

    def preprocess_image(self, img):
        """Preprocess image for the model"""
        # Resize image to 224x224
        img = img.resize((224, 224))
        # Convert to numpy array and ensure float32 type
        img_array = np.array(img, dtype=np.float32)
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        # Normalize pixel values
        img_array = img_array / 255.0
        return img_array

    def get_quality_score(self, img):
        """Get quality score for an image"""
        try:
            img_array = self.preprocess_image(img)
            # Get model predictions
            predictions = self.model(img_array)
            # Convert to numpy and get the highest confidence score
            scores = tf.nn.softmax(predictions).numpy()
            # Use the highest confidence as quality score
            quality_score = np.max(scores) * 10  # Scale to 0-10
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