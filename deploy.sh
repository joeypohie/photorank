#!/bin/bash

echo "🚀 PhotoRank Deployment Script"
echo "================================"

# Check if we're in the right directory
if [ ! -f "src/app.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed"
    exit 1
fi
cd ..

echo "✅ Frontend built successfully"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "⚠️  Heroku CLI not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install heroku/brew/heroku
    else
        echo "Please install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
fi

# Check if logged into Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku:"
    heroku login
fi

# Create or use existing Heroku app
echo "🌐 Setting up Heroku app..."
if [ -z "$HEROKU_APP_NAME" ]; then
    echo "Enter your Heroku app name (or press Enter to create a new one):"
    read app_name
    if [ -z "$app_name" ]; then
        app_name=$(heroku create --json | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
        echo "Created new app: $app_name"
    fi
else
    app_name=$HEROKU_APP_NAME
fi

# Set environment variables
echo "⚙️  Setting environment variables..."
heroku config:set FLASK_ENV=production --app $app_name
heroku config:set MAX_CONTENT_LENGTH=104857600 --app $app_name

# Deploy
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy to production" || git commit -m "Update deployment"
git push heroku main

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Your app is available at: https://$app_name.herokuapp.com"
    echo "📊 View logs with: heroku logs --tail --app $app_name"
else
    echo "❌ Deployment failed. Check the logs above."
    exit 1
fi
