# Deployment Guide for PhotoRank

This guide covers deploying your PhotoRank application to various platforms.

## Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Heroku Account**: Sign up at [heroku.com](https://heroku.com) (free tier available)
3. **Node.js**: Ensure you have Node.js installed locally

## Option 1: Heroku Deployment (Recommended)

### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Create Heroku App
```bash
heroku create your-photorank-app
```

### Step 4: Set Environment Variables
```bash
heroku config:set FLASK_ENV=production
heroku config:set MAX_CONTENT_LENGTH=104857600
```

### Step 5: Deploy Backend
```bash
git add .
git commit -m "Prepare for deployment"
git push heroku main
```

### Step 6: Deploy Frontend
```bash
cd frontend
npm run build
cd ..
git add frontend/build
git commit -m "Add frontend build"
git push heroku main
```

### Step 7: Open Your App
```bash
heroku open
```

## Option 2: Railway Deployment

### Step 1: Connect GitHub
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"

### Step 2: Configure Backend
1. Select your repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn src.app:app`
4. Add environment variables:
   - `FLASK_ENV=production`
   - `PORT=8000`

### Step 3: Deploy Frontend
1. Create another service for frontend
2. Set build command: `npm install && npm run build`
3. Set start command: `npx serve -s build -l 3000`

## Option 3: Vercel + Render

### Frontend (Vercel)
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set build command: `cd frontend && npm install && npm run build`
4. Set output directory: `frontend/build`

### Backend (Render)
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn src.app:app`
6. Add environment variables as needed

## Environment Variables

Set these in your deployment platform:

```bash
FLASK_ENV=production
PORT=8000
MAX_CONTENT_LENGTH=104857600
UPLOAD_FOLDER=uploads
```

## Troubleshooting

### Common Issues

1. **Build Failures**: Check that all dependencies are in `requirements.txt`
2. **Port Issues**: Ensure your platform sets the `PORT` environment variable
3. **Memory Issues**: PyTorch models can be memory-intensive; consider using smaller models for production
4. **File Upload Limits**: Adjust `MAX_CONTENT_LENGTH` based on your platform's limits

### Performance Optimization

1. **Model Caching**: Consider caching loaded models in production
2. **Image Processing**: Implement image compression for large uploads
3. **Database**: For production, consider using a proper database instead of in-memory storage

## Monitoring

- **Heroku**: Use `heroku logs --tail` to monitor your app
- **Railway**: View logs in the Railway dashboard
- **Vercel**: Check deployment status and logs in the Vercel dashboard

## Scaling Considerations

- **Memory**: PyTorch models require significant memory
- **Storage**: Consider using cloud storage (AWS S3, Google Cloud Storage) for uploaded images
- **Database**: Implement a proper database for production use
- **CDN**: Use a CDN for serving static frontend assets

## Security Notes

- **CORS**: Ensure CORS is properly configured for production domains
- **File Uploads**: Implement proper file validation and virus scanning
- **API Keys**: Never commit API keys to version control
- **HTTPS**: Ensure your deployment platform provides HTTPS
