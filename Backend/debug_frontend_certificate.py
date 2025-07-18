"""
Frontend Certificate Request Debugger
"""
import requests
import json

def test_frontend_like_request():
    """Test certificate generation mimicking frontend behavior"""
    
    # Test what frontend might be sending (with potential issues)
    test_cases = [
        {
            "name": "Working Backend Test",
            "data": {
                'analysis_id': 'test-123',
                'user_name': 'Test User',
                'waste_type': 'CATTLE MANURE',
                'co2_saved': 1250.75,
                'carbon_credits': 4.5,
                'processing_method': 'Anaerobic Digestion'
            }
        },
        {
            "name": "Frontend-like Request (potential string numbers)",
            "data": {
                'analysis_id': 'test-123',
                'user_name': 'Test User',
                'waste_type': 'CATTLE MANURE',
                'co2_saved': '1250.75',  # String instead of float
                'carbon_credits': '4.5',  # String instead of float
                'processing_method': 'Anaerobic Digestion'
            }
        },
        {
            "name": "Frontend-like Request (missing analysis_id)",
            "data": {
                'user_name': 'Test User',
                'waste_type': 'CATTLE MANURE',
                'co2_saved': 1250.75,
                'carbon_credits': 4.5,
                'processing_method': 'Anaerobic Digestion'
            }
        },
        {
            "name": "Frontend-like Request (null analysis_id)",
            "data": {
                'analysis_id': None,
                'user_name': 'Test User',
                'waste_type': 'CATTLE MANURE',
                'co2_saved': 1250.75,
                'carbon_credits': 4.5,
                'processing_method': 'Anaerobic Digestion'
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        print(f"Request data: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(
                'http://localhost:8000/api/generate-certificate',
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"✅ Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ Error Response: {response.text}")
                try:
                    error_json = response.json()
                    print(f"Error Details: {json.dumps(error_json, indent=2)}")
                except:
                    pass
            else:
                print("✅ Certificate generated successfully!")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed - Backend server not running")
            break
        except Exception as e:
            print(f'❌ Request failed: {e}')

if __name__ == "__main__":
    test_frontend_like_request()
