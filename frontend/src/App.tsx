import React, { useState } from 'react';
import './App.css';
import PhotoUpload from './components/PhotoUpload';
import ClusterView from './components/ClusterView';
import PhotoModal from './components/PhotoModal';
import { apiService, Photo, ClusteringResult } from './services/api';

function App() {
  const [clusteringResult, setClusteringResult] = useState<ClusteringResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedPhoto, setSelectedPhoto] = useState<Photo | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUploadComplete = async () => {
    setIsProcessing(true);
    setError(null);
    
    try {
      console.log('Processing photos for clustering...');
      const result = await apiService.processPhotos();
      setClusteringResult(result);
      console.log('Clustering complete:', result);
    } catch (err) {
      console.error('Processing failed:', err);
      setError(err instanceof Error ? err.message : 'Failed to process photos');
    } finally {
      setIsProcessing(false);
    }
  };

  const handlePhotoClick = (photo: Photo) => {
    setSelectedPhoto(photo);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedPhoto(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🧹 Image Ranker
          </h1>
          <p className="text-gray-600">
            Lazy to crawl through your photos?
          </p>
          <p className="text-gray-600">
            Upload your photos and let AI find the best one to keep
          </p>
        </header>

        {/* Main Content */}
        <main className="space-y-8">
          {/* Upload Section */}
          {!clusteringResult && (
            <section>
              {/* <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
                Upload Your Photos
              </h2> */}
              <PhotoUpload onUploadComplete={handleUploadComplete} />
            </section>
          )}

          {/* Processing State */}
          {isProcessing && (
            <section className="text-center py-12">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
              <h3 className="text-xl font-medium text-gray-700 mb-2">
                Processing your photos...
              </h3>
              <p className="text-gray-500">
                This may take a few minutes depending on the number of photos
              </p>
            </section>
          )}

          {/* Error Display */}
          {error && (
            <section className="bg-red-50 border border-red-200 rounded-lg p-6">
              <h3 className="text-lg font-medium text-red-800 mb-2">
                Error
              </h3>
              <p className="text-red-700">{error}</p>
              <button
                onClick={() => setError(null)}
                className="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
              >
                Dismiss
              </button>
            </section>
          )}

          {/* Results Section */}
          {clusteringResult && !isProcessing && (
            <section>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-semibold text-gray-800">
                  Clustering Results
                </h2>
                <button
                  onClick={() => setClusteringResult(null)}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Upload More Photos
                </button>
              </div>
              
              <ClusterView
                clusters={clusteringResult.clusters}
                unclustered={clusteringResult.unclustered}
                onPhotoClick={handlePhotoClick}
              />
            </section>
          )}
        </main>

        {/* Photo Modal */}
        <PhotoModal
          photo={selectedPhoto}
          isOpen={isModalOpen}
          onClose={closeModal}
        />
      </div>
    </div>
  );
}

export default App;
