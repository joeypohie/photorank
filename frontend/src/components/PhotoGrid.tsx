import React from 'react';
import { Photo } from '../services/api';

interface PhotoGridProps {
  photos: Photo[];
  onPhotoClick?: (photo: Photo) => void;
  showScores?: boolean;
  className?: string;
}

const PhotoGrid: React.FC<PhotoGridProps> = ({ 
  photos, 
  onPhotoClick, 
  showScores = false,
  className = ''
}) => {
  if (photos.length === 0) {
    return (
      <div className={`text-center py-12 ${className}`}>
        <p className="text-gray-500">No photos to display</p>
      </div>
    );
  }

  return (
    <div className={`grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 ${className}`}>
      {photos.map((photo) => (
        <div
          key={photo.id}
          className={`
            relative group cursor-pointer rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-all duration-200
            ${onPhotoClick ? 'hover:scale-105' : ''}
          `}
          onClick={() => onPhotoClick?.(photo)}
        >
          <img
            src={photo.url}
            alt={photo.filename}
            className="w-full h-48 object-cover"
            loading="lazy"
          />
          
          {showScores && photo.score !== undefined && (
            <div className="absolute top-2 right-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-sm font-medium">
              {photo.score.toFixed(1)}
            </div>
          )}
          
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-3 opacity-0 group-hover:opacity-100 transition-opacity">
            <p className="text-white text-sm truncate">{photo.filename}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PhotoGrid; 