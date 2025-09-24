from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from .photo_classifier import PhotoClassifier
from .utils import load_images, display_clusters
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
classifier = None  # Initialize lazily to save memory
processing_status = {"status": "idle", "message": "Ready to process photos"}

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
    global uploaded_photos, clustering_results, classifier, processing_status
    
    print("=== PROCESS ENDPOINT CALLED ===")
    print(f"Uploaded photos count: {len(uploaded_photos)}")
    
    if not uploaded_photos:
        print("ERROR: No photos uploaded")
        return jsonify({'error': 'No photos uploaded'}), 400
    
    try:
        processing_status = {"status": "processing", "message": "Initializing classifier..."}
        print("Starting photo processing...")
        
        # Initialize classifier lazily to save memory
        if classifier is None:
            print("Initializing PhotoClassifier...")
            # Use full version for Starter plan
            classifier = PhotoClassifier()
            print("PhotoClassifier initialized successfully")
        
        processing_status = {"status": "processing", "message": "Extracting features..."}
        # Extract images for clustering (only use the image data, not the full photo object)
        images = [(photo['filename'], photo['image']) for photo in uploaded_photos]
        print(f"Extracted {len(images)} images for clustering")
        
        processing_status = {"status": "processing", "message": "Clustering images..."}
        # Perform clustering
        print("Starting clustering...")
        cluster_groups = classifier.cluster_images(images)
        print(f"Clustering completed. Found {len(cluster_groups)} groups")
        
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
        
        processing_status = {"status": "completed", "message": "Processing completed successfully"}
        
        # Debug: Print the structure to see what might be causing issues - UPDATED
        print("Debug - Clustering results structure:")
        print(f"Number of clusters: {len(clusters)}")
        print(f"Number of unclustered: {len(unclustered)}")
        
        # Ensure no PIL Image objects are in the response
        def clean_for_json(obj):
            if isinstance(obj, dict):
                return {k: clean_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_for_json(item) for item in obj]
            elif hasattr(obj, '__dict__'):  # Check if it's a PIL Image or similar object
                return str(obj)
            else:
                return obj
        
        cleaned_results = clean_for_json(clustering_results)
        print("Debug - Cleaned clustering_results:", cleaned_results)
        
        print("About to create JSON response...")
        try:
            response = jsonify(cleaned_results)
            print("Debug - JSON response created successfully")
            print(f"Response size: {len(str(cleaned_results))} characters")
            return response
        except Exception as json_error:
            print(f"Debug - JSON serialization error: {json_error}")
            import traceback
            traceback.print_exc()
            # Return a simplified response without the problematic data
            simplified_results = {
                'clusters': [{'id': c['id'], 'photoCount': len(c['photos'])} for c in clusters],
                'unclustered': [{'id': p['id'], 'filename': p['filename']} for p in unclustered]
            }
            print("Returning simplified results")
            return jsonify(simplified_results)
        
    except Exception as e:
        print(f"Error processing photos: {str(e)}")
        import traceback
        traceback.print_exc()
        processing_status = {"status": "error", "message": f"Processing failed: {str(e)}"}
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
    
    photo = next((p for p in uploaded_photos if p['id'] == photo_id), None)
    
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

@app.route('/status', methods=['GET'])
def get_processing_status():
    global processing_status
    return jsonify(processing_status)

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint to verify backend is working"""
    return jsonify({
        'message': 'Backend is working',
        'photoCount': len(uploaded_photos),
        'timestamp': str(datetime.now())
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port) 