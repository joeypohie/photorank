# 🧹 PhotoRank - AI-Powered Photo Clustering & Ranking

An intelligent web application that automatically clusters similar photos and ranks them by quality using PyTorch and machine learning.

## ✨ Features

- **Smart Photo Clustering**: Groups similar photos using deep learning features
- **Quality Ranking**: Ranks photos within each cluster by quality and sharpness
- **Modern Web Interface**: Beautiful React frontend with drag-and-drop upload
- **PyTorch Backend**: Fast ML processing with ResNet50 and MobileNetV2
- **HEIC Support**: Handles modern iPhone photo formats

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/photorank.git
   cd photorank
   ```

2. **Set up Python backend**
   ```bash
   # Create virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start backend
   python src/app.py
   ```

3. **Set up React frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5001

## 🎯 How It Works

1. **Upload Photos**: Drag and drop multiple photos
2. **Feature Extraction**: PyTorch models extract deep learning features
3. **Clustering**: DBSCAN algorithm groups similar photos
4. **Quality Ranking**: Each cluster is ranked by quality and sharpness
5. **Results**: View organized clusters with recommended photos

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: Flask + PyTorch + scikit-learn
- **ML Models**: ResNet50 (features) + MobileNetV2 (quality)
- **Image Processing**: OpenCV + Pillow

## 📡 API Endpoints

- `POST /upload` - Upload photos
- `POST /process` - Process and cluster photos
- `GET /cluster` - Get clustering results
- `GET /health` - Health check
- `GET /` - API status

## 🚀 Deploy to Render

The easiest way to deploy PhotoRank is using Render's ML-friendly platform:

### One-Click Deploy

1. **Click the deploy button**:
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

2. **Connect your GitHub repository**
3. **Render automatically detects** the configuration
4. **Deploy in minutes!**

### Manual Deploy

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
2. **Create new Web Service**
3. **Connect your repository**
4. **Use the `render.yaml` configuration**

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.

## 🔧 Configuration

### Environment Variables

```bash
FLASK_ENV=production
MAX_CONTENT_LENGTH=104857600  # 100MB max file size
UPLOAD_FOLDER=uploads
PORT=8000  # Set by Render automatically
```

### Build Commands

```bash
# Backend
pip install -r requirements.txt
mkdir -p uploads

# Frontend
cd frontend
npm install
npm run build
```

## 📊 Performance

- **Build Time**: 5-10 minutes (first deploy), 2-3 minutes (subsequent)
- **Memory**: 1GB+ recommended for ML models
- **Response Time**: 2-5 seconds (cold start), 200-500ms (warm)
- **File Size**: Up to 100MB per photo

## 🚨 Troubleshooting

### Common Issues

1. **Build Timeout**: Upgrade to Starter plan ($7/month)
2. **Memory Issues**: Upgrade to Standard plan ($15/month)
3. **Model Download Failures**: Check internet, retry deployment

### Debug Commands

```bash
# Check build logs
render logs --service photorank-backend

# Check runtime logs
render logs --service photorank-backend --follow
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/photorank/issues)
- **Documentation**: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
- **Render Support**: [docs.render.com](https://docs.render.com/)

---

**Ready to deploy?** Click the "Deploy to Render" button above! 🚀 