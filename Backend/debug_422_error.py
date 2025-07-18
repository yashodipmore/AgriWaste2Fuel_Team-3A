"""
Debug 422 Error in Text Analysis - Quick Fix
"""
import requests
import json

def debug_text_analysis():
    """Debug the 422 error by checking what frontend is sending vs what backend expects"""
    
    print("🔍 DEBUGGING 422 ERROR IN TEXT ANALYSIS")
    print("=" * 50)
    
    # Test different payload formats to find what works
    test_cases = [
        {
            "name": "Current Frontend Format",
            "data": {
                "waste_type": "I have 1000 kg of cattle manure",
                "quantity": 1000,
                "location": "Maharashtra",
                "user_id": "test123",
                "timestamp": "2025-07-18T10:00:00.000Z"
            }
        },
        {
            "name": "Minimal Required Fields",
            "data": {
                "waste_type": "cattle manure 1000 kg"
            }
        },
        {
            "name": "With Optional Fields",
            "data": {
                "waste_type": "cattle manure 1000 kg",
                "quantity": 1000,
                "location": "Maharashtra"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        print(f"Payload: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(
                'http://localhost:8000/api/predict-text',
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ SUCCESS!")
                print(f"Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print(f"❌ FAILED: {response.text}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    print("\n🔧 CHECKING BACKEND SCHEMA...")
    # Let's check what the backend actually expects
    try:
        response = requests.get('http://localhost:8000/docs')
        if response.status_code == 200:
            print("✅ Backend is running - check /docs for schema")
        else:
            print("❌ Backend not responding")
    except:
        print("❌ Backend not running")
    
    return False

if __name__ == "__main__":
    debug_text_analysis()
