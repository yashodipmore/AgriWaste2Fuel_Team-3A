"""
Test certificate generation with frontend-like data after fix
"""
import requests
import json

def test_fixed_frontend_request():
    """Test certificate generation with properly parsed frontend data"""
    
    # Simulate what the fixed frontend should send
    # These values are what parseFloat(String(value).replace(/[^\d.-]/g, '')) should produce
    test_cases = [
        {
            "name": "Fixed Frontend Request - Normal Case",
            "data": {
                'analysis_id': 'test-123',
                'user_name': 'Test User',
                'waste_type': 'CATTLE MANURE',
                'co2_saved': 1250.75,  # Parsed from "1250.75 kg"
                'carbon_credits': 4.5,  # Parsed from "4.5 credits"
                'processing_method': 'Anaerobic Digestion'
            }
        },
        {
            "name": "Edge Case - Zero Values",
            "data": {
                'analysis_id': 'test-456',
                'user_name': 'Test User 2',
                'waste_type': 'Rice Straw',
                'co2_saved': 0.0,  # Parsed from invalid string
                'carbon_credits': 0.0,  # Parsed from invalid string
                'processing_method': 'Composting'
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
            
            if response.status_code == 200:
                print("✅ Certificate generated successfully!")
                print(f"Content Type: {response.headers.get('Content-Type')}")
                print(f"Content Length: {len(response.content)} bytes")
            else:
                print(f"❌ Status Code: {response.status_code}")
                print(f"Error Response: {response.text}")
                try:
                    error_json = response.json()
                    print(f"Error Details: {json.dumps(error_json, indent=2)}")
                except:
                    pass
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed - Backend server not running")
            break
        except Exception as e:
            print(f'❌ Request failed: {e}')

if __name__ == "__main__":
    test_fixed_frontend_request()
