import axios from 'axios';

// Use your actual backend URL in production
const API_BASE_URL = process.env.NODE_ENV === 'production' 
    ? 'https://photorank-backend.onrender.com'  // Replace with your actual backend URL
    : 'http://localhost:5001';

// Create axios instance with base configuration
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000, // 30 seconds for image processing
    headers: {
        'Content-Type': 'multipart/form-data',
    },
});

// Add request interceptor for debugging
apiClient.interceptors.request.use(
    (config) => {
        console.log(`Making ${config.method?.toUpperCase()} request to: ${config.baseURL}${config.url}`);
        return config;
    },
    (error) => {
        console.error('Request error:', error);
        return Promise.reject(error);
    }
);

// Add response interceptor for debugging
apiClient.interceptors.response.use(
    (response) => {
        console.log(`Response from ${response.config.url}:`, response.status);
        console.log('Response data:', response.data);
        return response;
    },
    (error) => {
        console.error('Response error:', error);
        return Promise.reject(error);
    }
);

export interface Photo {
    id: string;
    filename: string;
    url: string;
    score?: number;
}

export interface Cluster {
    id: number;
    photos: Photo[];
    recommendedPhoto: Photo;
}

export interface ClusteringResult {
    clusters: Cluster[];
    unclustered: Photo[];
}

class ApiService {
    async uploadPhotos(files: File[]): Promise<{ message: string; photoCount: number }> {
        const formData = new FormData();
        files.forEach(file => {
            formData.append('photos', file);
        });

        try {
            const response = await apiClient.post('/upload', formData);
            return response.data;
        } catch (error) {
            console.error('Upload error:', error);
            throw new Error('Failed to upload photos');
        }
    }

    async processPhotos(): Promise<ClusteringResult> {
        try {
            const response = await apiClient.post('/process');
            return response.data;
        } catch (error) {
            console.error('Processing error:', error);
            throw new Error('Failed to process photos');
        }
    }

    async getClusteringResults(): Promise<ClusteringResult> {
        try {
            const response = await apiClient.get('/cluster');
            return response.data;
        } catch (error) {
            console.error('Get results error:', error);
            throw new Error('Failed to get clustering results');
        }
    }

    async getPhoto(photoId: string): Promise<Photo> {
        try {
            const response = await apiClient.get(`/photos/${photoId}`);
            return response.data;
        } catch (error) {
            console.error('Get photo error:', error);
            throw new Error('Failed to get photo');
        }
    }

    async deletePhoto(photoId: string): Promise<void> {
        try {
            await apiClient.delete(`/photos/${photoId}`);
        } catch (error) {
            console.error('Delete photo error:', error);
            throw new Error('Failed to delete photo');
        }
    }

    async healthCheck(): Promise<{ status: string; photoCount: number }> {
        try {
            const response = await apiClient.get('/health');
            return response.data;
        } catch (error) {
            console.error('Health check error:', error);
            throw new Error('Health check failed');
        }
    }
}

export const apiService = new ApiService(); 