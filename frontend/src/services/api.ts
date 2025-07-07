import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Adjust this to match your backend URL

export interface Photo {
  id: string;
  filename: string;
  url: string;
  score?: number;
}

export interface Cluster {
  id: number;
  photos: Photo[];
  recommendedPhoto?: Photo;
}

export interface ClusteringResult {
  clusters: Cluster[];
  unclustered: Photo[];
}

class ApiService {
  private api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000, // 30 seconds for large uploads
  });

  // Upload photos to the backend
  async uploadPhotos(files: File[]): Promise<{ message: string; photoCount: number }> {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('photos', file);
    });

    const response = await this.api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  // Get clustering results
  async getClusteringResults(): Promise<ClusteringResult> {
    const response = await this.api.get('/cluster');
    return response.data;
  }

  // Process photos for clustering
  async processPhotos(): Promise<ClusteringResult> {
    const response = await this.api.post('/process');
    return response.data;
  }

  // Get individual photo
  async getPhoto(photoId: string): Promise<Photo> {
    const response = await this.api.get(`/photos/${photoId}`);
    return response.data;
  }

  // Delete photo
  async deletePhoto(photoId: string): Promise<void> {
    await this.api.delete(`/photos/${photoId}`);
  }
}

export const apiService = new ApiService(); 