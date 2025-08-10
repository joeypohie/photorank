# PhotoRank 🧹

An AI-powered photo ranking and clustering application that helps you find the best photos from your collection.

## Features

- **Smart Clustering**: Groups similar photos together using ResNet50 features
- **Quality Ranking**: Ranks photos within each cluster using MobileNetV2 and sharpness analysis
- **Modern UI**: Beautiful React frontend with drag-and-drop upload
- **AI-Powered**: Uses PyTorch for feature extraction and quality assessment

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- npm or yarn

### Local Development

1. **Clone and setup**
   ```bash
   git clone <your-repo-url>
   cd photorank
   ```

2. **Backend setup**
   ```bash
   python3.11 -m venv venv311
   source venv311/bin/activate
   pip install -r requirements.txt
   ```

3. **Frontend setup**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Run the application**
   ```bash
   # Terminal 1: Backend
   source venv311/bin/activate
   python src/app.py
   
   # Terminal 2: Frontend
   cd frontend
   npm start
   ```

5. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5001

## Deployment Options

### 🚀 Heroku (Recommended for beginners)
```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Deploy with one command
./deploy.sh
```

### 🐳 Docker
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### 🌐 Railway
1. Connect your GitHub repo to [Railway](https://railway.app)
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn src.app:app`

### 📱 Vercel + Render
- **Frontend**: Deploy to [Vercel](https://vercel.com)
- **Backend**: Deploy to [Render](https://render.com)

## Architecture

- **Backend**: Flask + PyTorch (ResNet50 + MobileNetV2)
- **Frontend**: React + TypeScript + Tailwind CSS
- **ML Models**: Pre-trained PyTorch models for feature extraction and quality assessment
- **Storage**: Local file storage (configurable for cloud storage)

## API Endpoints

- `POST /upload` - Upload photos
- `POST /process` - Process photos for clustering
- `GET /cluster` - Get clustering results
- `GET /health` - Health check
- `GET /photos/<id>` - Get specific photo
- `DELETE /photos/<id>` - Delete photo

## Environment Variables

- `FLASK_ENV` - Set to 'production' for deployment
- `PORT` - Server port (default: 5001)
- `MAX_CONTENT_LENGTH` - Max file upload size (default: 100MB)
- `UPLOAD_FOLDER` - Directory for uploaded files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For deployment help, see [DEPLOYMENT.md](DEPLOYMENT.md) 