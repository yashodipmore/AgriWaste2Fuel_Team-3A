"""
Firebase Token Generator for Testing
This script helps generate a Firebase token for testing backend authentication.
"""

import json
import requests
from datetime import datetime

def test_with_manual_token():
    """
    Test backend with manually provided Firebase token
    """
    print("🔥 FIREBASE TOKEN TESTING")
    print("=" * 60)
    print(f"Testing Time: {datetime.now()}")
    print("=" * 60)
    
    # Instructions for getting token
    print("📋 To get Firebase token from frontend:")
    print("1. Login to your React frontend")
    print("2. Open browser console (F12)")
    print("3. Run this JavaScript code:")
    print()
    print("JavaScript Code:")
    print("-" * 40)
    print("""
import { getAuth } from 'firebase/auth';

const auth = getAuth();
const user = auth.currentUser;

if (user) {
    user.getIdToken().then(token => {
        console.log('Firebase Token:', token);
        // Copy this token for testing
    });
} else {
    console.log('No user logged in');
}
    """)
    print("-" * 40)
    print()
    print("4. Copy the token and run:")
    print("   python test_with_token.py --token YOUR_COPIED_TOKEN")
    print()
    
    # Test endpoints without token (development mode)
    print("🔓 Testing Development Mode (No Token)")
    print("-" * 50)
    
    base_url = "http://localhost:8000/api/v1"
    
    try:
        # Test auth status
        response = requests.get(f"{base_url}/auth/status")
        print(f"Auth Status: {response.status_code}")
        result = response.json()
        print(f"Authenticated: {result.get('authenticated')}")
        print(f"Message: {result.get('message')}")
        
        # Test protected endpoint
        params = {
            "user_id": "test_user",
            "co2_saved": 50,
            "waste_type": "Rice Straw",
            "processing_method": "biogas"
        }
        response = requests.get(f"{base_url}/generate-certificate", params=params)
        print(f"Certificate Generation: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Certificate ID: {result.get('certificate_id')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    test_with_manual_token()
