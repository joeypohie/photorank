import React from 'react';
import { Photo } from '../services/api';

interface PhotoModalProps {
  photo: Photo | null;
  isOpen: boolean;
  onClose: () => void;
}

const PhotoModal: React.FC<PhotoModalProps> = ({ photo, isOpen, onClose }) => {
  if (!isOpen || !photo) return null;

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      <div className="bg-white rounded-lg max-w-4xl max-h-full overflow-hidden">
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="text-lg font-semibold text-gray-800">
            {photo.filename}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
          >
            ×
          </button>
        </div>
        
        <div className="p-4">
          <div className="flex flex-col lg:flex-row gap-6">
            <div className="flex-1">
              <img
                src={photo.url}
                alt={photo.filename}
                className="w-full h-auto max-h-96 object-contain rounded-lg"
              />
            </div>
            
            <div className="lg:w-64 space-y-4">
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Photo Details</h4>
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="text-gray-600">Filename:</span>
                    <p className="font-medium">{photo.filename}</p>
                  </div>
                  {photo.score !== undefined && (
                    <div>
                      <span className="text-gray-600">Quality Score:</span>
                      <p className="font-medium text-lg text-blue-600">
                        {photo.score.toFixed(1)}
                      </p>
                    </div>
                  )}
                </div>
              </div>
              
              <div className="pt-4 border-t">
                <button
                  onClick={onClose}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PhotoModal; 