"""
Test script for certificate generation debugging
"""
import requests
import json

def test_certificate_generation():
    """Test certificate generation with proper data"""
    
    # Test certificate data
    certificate_data = {
        'analysis_id': 'test-123',
        'user_name': 'Test User',
        'waste_type': 'CATTLE MANURE',
        'co2_saved': 1250.75,
        'carbon_credits': 4.5,
        'processing_method': 'Anaerobic Digestion'
    }
    
    print("Testing certificate generation...")
    print(f"Request data: {json.dumps(certificate_data, indent=2)}")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/generate-certificate',
            json=certificate_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f'\nStatus Code: {response.status_code}')
        
        if response.status_code != 200:
            print(f'Error Response: {response.text}')
            try:
                error_json = response.json()
                print(f'Error Details: {json.dumps(error_json, indent=2)}')
            except:
                pass
        else:
            print('Certificate generated successfully!')
            print(f'Content Type: {response.headers.get("Content-Type")}')
            print(f'Content Length: {len(response.content)} bytes')
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend server not running on localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Request timeout - Server took too long to respond")
    except Exception as e:
        print(f'❌ Request failed: {e}')

if __name__ == "__main__":
    test_certificate_generation()
