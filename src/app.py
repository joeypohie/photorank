from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from photo_classifier import PhotoClassifier
from utils import load_images, display_clusters
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic'}
MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))  # 100MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables to store uploaded photos and results
uploaded_photos = []
clustering_results = None
classifier = PhotoClassifier()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

@app.route('/upload', methods=['POST'])
def upload_photos():
    global uploaded_photos
    
    if 'photos' not in request.files:
        return jsonify({'error': 'No photos provided'}), 400
    
    files = request.files.getlist('photos')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    uploaded_count = 0
    
    for file in files:
        if file and allowed_file(file.filename):
            try:
                # Generate unique filename
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                # Save file
                file.save(filepath)
                
                # Load image and convert to base64
                image = Image.open(filepath)
                
                # Create photo object
                photo = {
                    'id': str(uuid.uuid4()),
                    'filename': filename,
                    'url': image_to_base64(image),
                    'filepath': filepath,
                    'image': image
                }
                
                uploaded_photos.append(photo)
                uploaded_count += 1
                
            except Exception as e:
                print(f"Error processing {file.filename}: {str(e)}")
                continue
    
    return jsonify({
        'message': f'Successfully uploaded {uploaded_count} photos',
        'photoCount': uploaded_count
    })

@app.route('/process', methods=['POST'])
def process_photos():
    global uploaded_photos, clustering_results
    
    if not uploaded_photos:
        return jsonify({'error': 'No photos uploaded'}), 400
    
    try:
        # Extract images for clustering
        images = [(photo['filename'], photo['image']) for photo in uploaded_photos]
        
        # Perform clustering
        cluster_groups = classifier.cluster_images(images)
        
        # Convert results to frontend format
        clusters = []
        unclustered = []
        
        for cluster_id, ranked_images in cluster_groups.items():
            if cluster_id == -1:  # Unclustered images
                for filename, score in ranked_images:
                    photo = next((p for p in uploaded_photos if p['filename'] == filename), None)
                    if photo:
                        unclustered.append({
                            'id': photo['id'],
                            'filename': photo['filename'],
                            'url': photo['url'],
                            'score': float(score) if score is not None else None
                        })
            else:  # Clustered images
                cluster_photos = []
                recommended_photo = None
                
                for filename, score in ranked_images:
                    photo = next((p for p in uploaded_photos if p['filename'] == filename), None)
                    if photo:
                        photo_obj = {
                            'id': photo['id'],
                            'filename': photo['filename'],
                            'url': photo['url'],
                            'score': float(score) if score is not None else None
                        }
                        cluster_photos.append(photo_obj)
                        
                        # First photo is the recommended one
                        if not recommended_photo:
                            recommended_photo = photo_obj
                
                clusters.append({
                    'id': int(cluster_id),
                    'photos': cluster_photos,
                    'recommendedPhoto': recommended_photo
                })
        
        clustering_results = {
            'clusters': clusters,
            'unclustered': unclustered
        }
        
        # Debug: Print the structure to see what might be causing issues - UPDATED
        print("Debug - Clustering results structure:")
        print(f"Number of clusters: {len(clusters)}")
        print(f"Number of unclustered: {len(unclustered)}")
        
        return jsonify(clustering_results)
        
    except Exception as e:
        print(f"Error processing photos: {str(e)}")
        return jsonify({'error': 'Failed to process photos'}), 500

@app.route('/cluster', methods=['GET'])
def get_clustering_results():
    global clustering_results
    
    if clustering_results is None:
        return jsonify({'error': 'No clustering results available'}), 404
    
    return jsonify(clustering_results)

@app.route('/photos/<photo_id>', methods=['GET'])
def get_photo(photo_id):
    global uploaded_photos
    
    photo = next((p for p in uploaded_photos if p['id'] == photo_id), None)
    
    if not photo:
        return jsonify({'error': 'Photo not found'}), 404
    
    return jsonify({
        'id': photo['id'],
        'filename': photo['filename'],
        'url': photo['url']
    })

@app.route('/photos/<photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    global uploaded_photos
    
    photo = next((p for p in uploaded_photos if p['id'] != photo_id), None)
    
    if not photo:
        return jsonify({'error': 'Photo not found'}), 404
    
    try:
        # Remove file from disk
        if os.path.exists(photo['filepath']):
            os.remove(photo['filepath'])
        
        # Remove from uploaded_photos list
        uploaded_photos = [p for p in uploaded_photos if p['id'] != photo_id]
        
        return jsonify({'message': 'Photo deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': f'Failed to delete photo: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'photoCount': len(uploaded_photos)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port) 