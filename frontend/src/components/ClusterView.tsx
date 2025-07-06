import React, { useState } from 'react';
import { Cluster, Photo } from '../services/api';
import PhotoGrid from './PhotoGrid';

interface ClusterViewProps {
  clusters: Cluster[];
  unclustered: Photo[];
  onPhotoClick?: (photo: Photo) => void;
}

const ClusterView: React.FC<ClusterViewProps> = ({ 
  clusters, 
  unclustered, 
  onPhotoClick 
}) => {
  const [expandedClusters, setExpandedClusters] = useState<Set<number>>(new Set());

  const toggleCluster = (clusterId: number) => {
    const newExpanded = new Set(expandedClusters);
    if (newExpanded.has(clusterId)) {
      newExpanded.delete(clusterId);
    } else {
      newExpanded.add(clusterId);
    }
    setExpandedClusters(newExpanded);
  };

  return (
    <div className="space-y-8">
      {/* Clusters */}
      {clusters.map((cluster) => (
        <div key={cluster.id} className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-xl font-semibold text-gray-800">
                Cluster {cluster.id}
              </h3>
              <p className="text-gray-600">
                {cluster.photos.length} similar photos
              </p>
            </div>
            
            {cluster.recommendedPhoto && (
              <div className="text-right">
                <p className="text-sm text-gray-600">Recommended to keep:</p>
                <p className="font-medium text-green-600">
                  {cluster.recommendedPhoto.filename}
                  {cluster.recommendedPhoto.score && (
                    <span className="ml-2 text-sm text-gray-500">
                      (Score: {cluster.recommendedPhoto.score.toFixed(1)})
                    </span>
                  )}
                </p>
              </div>
            )}
          </div>

          {/* Show recommended photo prominently */}
          {cluster.recommendedPhoto && (
            <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm font-medium text-green-800 mb-2">
                🏆 Best photo in this cluster:
              </p>
              <div className="flex items-center space-x-4">
                <img
                  src={cluster.recommendedPhoto.url}
                  alt={cluster.recommendedPhoto.filename}
                  className="w-24 h-24 object-cover rounded-lg"
                  onClick={() => onPhotoClick?.(cluster.recommendedPhoto!)}
                />
                <div>
                  <p className="font-medium">{cluster.recommendedPhoto.filename}</p>
                  {cluster.recommendedPhoto.score && (
                    <p className="text-sm text-gray-600">
                      Quality score: {cluster.recommendedPhoto.score.toFixed(1)}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* All photos in cluster */}
          <div>
            <button
              onClick={() => toggleCluster(cluster.id)}
              className="text-blue-600 hover:text-blue-800 text-sm font-medium mb-3"
            >
              {expandedClusters.has(cluster.id) ? 'Hide' : 'Show'} all photos in cluster
            </button>
            
            {expandedClusters.has(cluster.id) && (
              <PhotoGrid
                photos={cluster.photos}
                onPhotoClick={onPhotoClick}
                showScores={true}
              />
            )}
          </div>
        </div>
      ))}

      {/* Unclustered photos */}
      {unclustered.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            Unclustered Photos
          </h3>
          <p className="text-gray-600 mb-4">
            {unclustered.length} photos that don't have similar matches
          </p>
          <PhotoGrid
            photos={unclustered}
            onPhotoClick={onPhotoClick}
            showScores={true}
          />
        </div>
      )}

      {/* Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-800 mb-2">Summary</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <span className="font-medium">Total clusters:</span> {clusters.length}
          </div>
          <div>
            <span className="font-medium">Total photos:</span> {clusters.reduce((sum, c) => sum + c.photos.length, 0) + unclustered.length}
          </div>
          <div>
            <span className="font-medium">Unclustered:</span> {unclustered.length}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClusterView; 