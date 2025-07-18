"""
Test script for image upload endpoint
"""

import requests
import json
from datetime import datetime
import os

# API Base URL
BASE_URL = "http://localhost:8000/api/v1"

def create_test_image():
    """Create a simple test image for upload testing"""
    from PIL import Image
    import io
    
    # Create a simple 500x500 RGB image
    img = Image.new('RGB', (500, 500), color='green')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def test_image_upload():
    """Test image upload endpoint"""
    print("🖼️  Testing Image Upload Endpoint")
    print("=" * 50)
    
    try:
        # Create test image
        test_image_data = create_test_image()
        
        # Prepare file upload
        files = {
            'file': ('test_waste.jpg', test_image_data, 'image/jpeg')
        }
        
        # Optional form data
        data = {
            'user_id': 'test_user_123',
            'location': 'Test Farm, Punjab'
        }
        
        # Make request
        response = requests.post(f"{BASE_URL}/predict-image", files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Image Upload: SUCCESS")
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Image Upload: FAILED")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Image Upload: ERROR - {str(e)}")
    
    print("-" * 50)

def test_supported_formats():
    """Test supported formats endpoint"""
    print("📋 Testing Supported Formats Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/supported-formats")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Supported Formats: SUCCESS")
            print(f"Supported formats: {result['supported_formats']}")
            print(f"Max file size: {result['max_file_size_mb']} MB")
        else:
            print(f"❌ Supported Formats: FAILED")
            
    except Exception as e:
        print(f"❌ Supported Formats: ERROR - {str(e)}")
    
    print("-" * 50)

def test_classification_categories():
    """Test classification categories endpoint"""
    print("📊 Testing Classification Categories Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/classification-categories")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Classification Categories: SUCCESS")
            print(f"Total waste types: {result['total_waste_types']}")
            print(f"Categories: {list(result['categories'].keys())}")
        else:
            print(f"❌ Classification Categories: FAILED")
            
    except Exception as e:
        print(f"❌ Classification Categories: ERROR - {str(e)}")
    
    print("-" * 50)

def test_all_endpoints():
    """Test all image-related endpoints"""
    print("🚀 Testing All Image Processing Endpoints")
    print("=" * 60)
    print(f"Testing at: {datetime.now()}")
    print("=" * 60)
    
    # Test image upload
    test_image_upload()
    
    # Test supporting endpoints
    test_supported_formats()
    test_classification_categories()
    
    print("🎉 Image endpoint testing completed!")

if __name__ == "__main__":
    test_all_endpoints()
