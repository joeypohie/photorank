import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { apiService } from '../services/api';

interface PhotoUploadProps {
  onUploadComplete: () => void;
}

const PhotoUpload: React.FC<PhotoUploadProps> = ({ onUploadComplete }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    setIsUploading(true);
    setError(null);
    setUploadProgress(0);

    try {
      // Filter for image files
      const imageFiles = acceptedFiles.filter(file => 
        file.type.startsWith('image/') || 
        file.name.toLowerCase().endsWith('.heic')
      );

      if (imageFiles.length === 0) {
        throw new Error('No valid image files found. Please select PNG, JPG, JPEG, or HEIC files.');
      }

      console.log(`Uploading ${imageFiles.length} images...`);
      
      // Simulate progress (since we don't have actual progress from the API yet)
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90));
      }, 200);

      const result = await apiService.uploadPhotos(imageFiles);
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      console.log('Upload successful:', result);
      onUploadComplete();
      
      // Reset after a short delay
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
      }, 1000);

    } catch (err) {
      console.error('Upload failed:', err);
      setError(err instanceof Error ? err.message : 'Upload failed. Please try again.');
      setIsUploading(false);
      setUploadProgress(0);
    }
  }, [onUploadComplete]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'image/heic': ['.heic']
    },
    multiple: true,
    disabled: isUploading
  });

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
          }
          ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {isUploading ? (
          <div className="space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="text-lg font-medium text-gray-700">Uploading photos...</p>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-500">{uploadProgress}% complete</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-6xl text-gray-400">📸</div>
            <div>
              <p className="text-xl font-medium text-gray-700">
                {isDragActive ? 'Drop photos here' : 'Upload your photos'}
              </p>
              <p className="text-gray-500 mt-2">
                Drag and drop photos here, or click to select files
              </p>
              <p className="text-sm text-gray-400 mt-1">
                Supports PNG, JPG, JPEG, and HEIC files
              </p>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700">{error}</p>
        </div>
      )}
    </div>
  );
};

export default PhotoUpload; 