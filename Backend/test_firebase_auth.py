"""
Test Firebase Authentication Integration
"""

import requests
import json
from datetime import datetime

# Base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_auth_status_anonymous():
    """Test auth status without token (anonymous)"""
    print("🔓 Testing Anonymous Auth Status")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/auth/status")
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Authenticated: {result.get('authenticated')}")
        print(f"User: {result.get('user')}")
        print(f"Message: {result.get('message')}")
    except Exception as e:
        print(f"❌ Anonymous Auth Status Failed: {e}")
    
    print("-" * 50)

def test_auth_with_token(token):
    """Test auth with Firebase token"""
    print("🔐 Testing Firebase Token Authentication")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test auth status
    try:
        response = requests.get(f"{BASE_URL}/auth/status", headers=headers)
        print(f"✅ Auth Status: {response.status_code}")
        result = response.json()
        print(f"Authenticated: {result.get('authenticated')}")
        if result.get('user'):
            user = result.get('user')
            print(f"User ID: {user.get('uid')}")
            print(f"Email: {user.get('email')}")
            print(f"Name: {user.get('name')}")
    except Exception as e:
        print(f"❌ Auth Status Failed: {e}")
    
    # Test user profile
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        print(f"✅ User Profile: {response.status_code}")
        result = response.json()
        print(f"UID: {result.get('uid')}")
        print(f"Email: {result.get('email')}")
        print(f"Name: {result.get('name')}")
        print(f"Email Verified: {result.get('email_verified')}")
    except Exception as e:
        print(f"❌ User Profile Failed: {e}")
    
    # Test token verification
    try:
        response = requests.post(f"{BASE_URL}/auth/verify-token", headers=headers)
        print(f"✅ Token Verification: {response.status_code}")
        result = response.json()
        print(f"Valid: {result.get('valid')}")
    except Exception as e:
        print(f"❌ Token Verification Failed: {e}")
    
    print("-" * 50)

def test_protected_endpoints_with_auth(token):
    """Test protected endpoints with authentication"""
    print("🛡️ Testing Protected Endpoints with Auth")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test certificate generation with auth
    test_params = {
        "user_id": "authenticated_user",
        "co2_saved": 63.5,
        "waste_type": "Rice Straw",
        "processing_method": "biogas"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/generate-certificate", params=test_params, headers=headers)
        print(f"✅ Certificate Generation (Authenticated): {response.status_code}")
        result = response.json()
        print(f"Certificate ID: {result.get('certificate_id')}")
    except Exception as e:
        print(f"❌ Certificate Generation Failed: {e}")
    
    print("-" * 50)

def run_auth_tests(firebase_token=None):
    """Run complete authentication test suite"""
    print("🔥 FIREBASE AUTHENTICATION TESTS")
    print("=" * 60)
    print(f"Testing Time: {datetime.now()}")
    print("=" * 60)
    
    # Test anonymous access
    test_auth_status_anonymous()
    
    if firebase_token:
        # Test with Firebase token
        test_auth_with_token(firebase_token)
        test_protected_endpoints_with_auth(firebase_token)
    else:
        print("⚠️ No Firebase token provided - Testing development mode")
        print("🚀 To test with real Firebase token:")
        print("   python test_firebase_auth.py --token YOUR_FIREBASE_TOKEN")
        print()
        print("📋 Next Steps:")
        print("1. Get Firebase config from Firebase Console")
        print("2. Create service account key or use environment variables")
        print("3. Get user token from frontend Firebase auth")
        print("4. Test with real token")
    
    print("=" * 60)

if __name__ == "__main__":
    import sys
    
    # Check for token argument
    firebase_token = None
    if len(sys.argv) > 2 and sys.argv[1] == "--token":
        firebase_token = sys.argv[2]
    
    run_auth_tests(firebase_token)
