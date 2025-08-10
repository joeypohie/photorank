# 🚀 Deploy PhotoRank to Render

Render is an excellent choice for PyTorch applications because it provides:
- **Better ML model support** than Railway
- **Longer build times** for downloading models
- **More memory** for running ML workloads
- **Automatic scaling** and health checks

## 📋 Prerequisites

1. **GitHub Account** with your PhotoRank repository
2. **Render Account** (free tier available)
3. **PyTorch Models** (will be downloaded during build)

## 🚀 Quick Deploy

### Option 1: One-Click Deploy (Recommended)

1. **Click this button** to deploy directly:
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

2. **Connect your GitHub repository**
3. **Select the repository**: `yourusername/photorank`
4. **Render will automatically detect** the `render.yaml` configuration

### Option 2: Manual Deploy

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service** (see configuration below)

## ⚙️ Configuration

### Backend Service (Python/Flask)

```yaml
Name: photorank-backend
Runtime: Python 3
Build Command: pip install -r requirements.txt && mkdir -p uploads
Start Command: gunicorn src.app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300
Plan: Starter ($7/month) - Recommended for ML models
```

**Environment Variables:**
```bash
FLASK_ENV=production
MAX_CONTENT_LENGTH=104857600
UPLOAD_FOLDER=uploads
```

### Frontend Service (Static Site)

```yaml
Name: photorank-frontend
Runtime: Static Site
Build Command: cd frontend && npm install && npm run build
Publish Directory: frontend/build
```

## 🔧 Build Process

### What Happens During Build:

1. **Python Environment Setup**
   - Python 3.11 installation
   - pip package installation

2. **PyTorch Model Download**
   - MobileNetV2 (feature extraction)
   - ResNet50 (quality assessment)
   - Models cached for faster subsequent builds

3. **Dependencies Installation**
   - All packages from `requirements.txt`
   - OpenCV, scikit-learn, PIL, etc.

4. **Application Setup**
   - Create uploads directory
   - Configure environment variables

## 📊 Performance & Scaling

### Memory Usage:
- **Free Tier**: 512MB (not recommended for ML)
- **Starter Plan**: 1GB (good for PyTorch)
- **Standard Plan**: 2GB (excellent for ML workloads)

### Build Time:
- **First Deploy**: 5-10 minutes (model download)
- **Subsequent Deploys**: 2-3 minutes (cached models)

### Response Time:
- **Cold Start**: 2-5 seconds (model loading)
- **Warm Start**: 200-500ms (cached models)

## 🚨 Troubleshooting

### Common Issues:

#### 1. **Build Timeout**
```
Error: Build exceeded maximum time limit
```
**Solution**: Upgrade to Starter plan ($7/month) for longer build times

#### 2. **Memory Issues**
```
Error: Process ran out of memory
```
**Solution**: Upgrade to Standard plan ($15/month) for more memory

#### 3. **Model Download Failures**
```
Error: Failed to download PyTorch models
```
**Solution**: Check internet connectivity, retry deployment

#### 4. **Import Errors**
```
Error: No module named 'torch'
```
**Solution**: Ensure `requirements.txt` has correct PyTorch versions

### Debug Commands:

```bash
# Check build logs
render logs --service photorank-backend

# Check runtime logs
render logs --service photorank-backend --follow

# SSH into service (if needed)
render shell --service photorank-backend
```

## 🔄 Continuous Deployment

### Automatic Deploys:
- **Enabled by default** with `autoDeploy: true`
- **Triggers on** every push to main branch
- **Builds and deploys** automatically

### Manual Deploys:
```bash
# Trigger manual deploy
render deploy --service photorank-backend

# Deploy specific commit
render deploy --service photorank-backend --commit abc123
```

## 💰 Cost Breakdown

### Free Tier:
- **Backend**: ❌ Not suitable for ML models
- **Frontend**: ✅ Static sites work fine

### Starter Plan ($7/month):
- **Backend**: ✅ Good for ML models
- **Frontend**: ✅ Static sites included
- **Total**: $7/month

### Standard Plan ($15/month):
- **Backend**: ✅ Excellent for ML models
- **Frontend**: ✅ Static sites included
- **Total**: $15/month

## 🎯 Next Steps

1. **Deploy to Render** using the guide above
2. **Test the application** with sample photos
3. **Monitor performance** in Render dashboard
4. **Scale up** if needed (more memory/CPU)

## 📞 Support

- **Render Documentation**: [docs.render.com](https://docs.render.com/)
- **Community Forum**: [community.render.com](https://community.render.com/)
- **Email Support**: Available on paid plans

---

**Ready to deploy?** Click the "Deploy to Render" button above or follow the manual steps! 🚀
