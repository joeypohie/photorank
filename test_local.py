#!/usr/bin/env python3
"""
Test script for PhotoRank local development
"""
import requests
import json
import os
from pathlib import Path

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get('http://localhost:5001/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is healthy: {data}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Start it with:")
        print("   cd src && python -c \"from photorank.app import app; app.run(debug=True, host='0.0.0.0', port=5001)\"")
        return False

def test_frontend():
    """Test if frontend is running"""
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            print("✅ Frontend is running at http://localhost:3000")
            return True
        else:
            print(f"❌ Frontend check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running. Start it with:")
        print("   cd frontend && npm start")
        return False

def test_photo_upload():
    """Test photo upload functionality"""
    # Check if we have test photos
    uploads_dir = Path("uploads")
    if not uploads_dir.exists() or not any(uploads_dir.iterdir()):
        print("⚠️  No test photos found in uploads/ directory")
        print("   Add some photos to the uploads/ directory to test upload functionality")
        return False
    
    # Get a test photo
    test_photo = next(uploads_dir.iterdir())
    print(f"📸 Testing with photo: {test_photo.name}")
    
    try:
        with open(test_photo, 'rb') as f:
            files = {'photos': (test_photo.name, f, 'image/jpeg')}
            response = requests.post('http://localhost:5001/upload', files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Photo upload successful: {data}")
            return True
        else:
            print(f"❌ Photo upload failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Photo upload error: {e}")
        return False

def main():
    print("🧪 Testing PhotoRank Local Development Environment")
    print("=" * 50)
    
    # Test backend
    print("\n1. Testing Backend...")
    backend_ok = test_backend_health()
    
    # Test frontend
    print("\n2. Testing Frontend...")
    frontend_ok = test_frontend()
    
    # Test photo upload if backend is running
    if backend_ok:
        print("\n3. Testing Photo Upload...")
        test_photo_upload()
    
    print("\n" + "=" * 50)
    if backend_ok and frontend_ok:
        print("🎉 Local development environment is ready!")
        print("\n📱 Access your app at:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://localhost:5001")
        print("\n🔧 To test the full workflow:")
        print("   1. Open http://localhost:3000 in your browser")
        print("   2. Upload some photos")
        print("   3. Click 'Process Photos' to see clustering results")
    else:
        print("❌ Some services are not running. Check the errors above.")

if __name__ == "__main__":
    main()
