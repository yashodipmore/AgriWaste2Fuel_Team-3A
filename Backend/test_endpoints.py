"""
Test script to verify all API endpoints are working
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_predict_text():
    """Test text prediction endpoint"""
    url = f"{BASE_URL}/predict-text"
    data = {
        "waste_type": "rice straw",
        "quantity": 1000
    }
    response = requests.post(url, json=data)
    print(f"✅ Text Prediction: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_recommend():
    """Test recommendation endpoint"""
    url = f"{BASE_URL}/recommend"
    data = {
        "waste_type": "Rice Straw",
        "quantity": 1000
    }
    response = requests.post(url, json=data)
    print(f"✅ Recommendation: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_ghg_savings():
    """Test GHG calculation endpoint"""
    url = f"{BASE_URL}/ghg-savings"
    data = {
        "waste_type": "Rice Straw",
        "processing_method": "biogas",
        "quantity": 1000
    }
    response = requests.post(url, json=data)
    print(f"✅ GHG Calculation: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_carbon_credit():
    """Test carbon credit endpoint"""
    url = f"{BASE_URL}/carbon-credit"
    data = {
        "co2_saved": 2.5,
        "waste_type": "Rice Straw",
        "processing_method": "biogas"
    }
    response = requests.post(url, json=data)
    print(f"✅ Carbon Credit: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

if __name__ == "__main__":
    print("🚀 Testing AgriWaste2Fuel API Endpoints")
    print("=" * 50)
    
    try:
        test_predict_text()
        test_recommend()
        test_ghg_savings()
        test_carbon_credit()
        print("🎉 All endpoints tested successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
