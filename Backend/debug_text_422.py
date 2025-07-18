"""
Debug text analysis 422 error
"""
import requests
import json

def debug_text_analysis():
    """Debug the 422 error in text analysis"""
    
    print("🔍 DEBUGGING TEXT ANALYSIS 422 ERROR")
    print("=" * 50)
    
    # Test with exact frontend data format
    test_cases = [
        {
            "name": "Frontend Format 1",
            "data": {
                "waste_type": "I have cattle manure from my farm",
                "quantity": 1000,
                "location": "Maharashtra",
                "user_id": "test-user"
            }
        },
        {
            "name": "Frontend Format 2", 
            "data": {
                "waste_type": "cattle manure",
                "quantity": 1000,
                "location": "Maharashtra"
            }
        },
        {
            "name": "Minimal Format",
            "data": {
                "waste_type": "cattle manure"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        print(f"Data: {json.dumps(test_case['data'], indent=2)}")
        
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
                print(f"✅ SUCCESS")
                print(f"   Classified: {result.get('waste_type', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 'N/A')}")
            else:
                print(f"❌ FAILED")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    # Test recommendations endpoint too
    print(f"\n🧪 Testing Recommendations with simple data")
    rec_data = {
        "waste_type": "CATTLE MANURE",
        "quantity": 1000,
        "location": "Maharashtra"
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/recommend',
            json=rec_data,
            timeout=10
        )
        print(f"Recommendations Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Recommendations Error: {response.text}")
        else:
            print("✅ Recommendations working")
    except Exception as e:
        print(f"❌ Recommendations Exception: {e}")

if __name__ == "__main__":
    debug_text_analysis()
