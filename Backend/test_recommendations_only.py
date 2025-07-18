"""
Test the recommendations endpoint separately to identify timeout issue
"""
import requests
import json
import time

def test_recommendations_only():
    """Test just the recommendations endpoint with proper data"""
    
    # Test recommendation data
    rec_data = {
        'waste_type': 'CATTLE MANURE',
        'quantity': 1000.0,
        'location': 'Maharashtra',
        'moisture_content': 70.0
    }
    
    print("Testing recommendations endpoint only...")
    print(f"Request data: {json.dumps(rec_data, indent=2)}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            'http://localhost:8000/api/recommend',
            json=rec_data,
            headers={'Content-Type': 'application/json'},
            timeout=30  # Increased timeout
        )
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        print(f'\nStatus Code: {response.status_code}')
        print(f'Response Time: {response_time}s')
        
        if response.status_code == 200:
            result = response.json()
            print('✅ Recommendations successful!')
            print(f"Recommended Method: {result.get('recommended_method', 'N/A')}")
            print(f"Processing Time: {result.get('processing_time', 'N/A')}")
            print(f"Efficiency: {result.get('efficiency', 'N/A')}%")
        else:
            print(f'❌ Error Response: {response.text}')
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - Recommendations taking too long")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend server not running")
    except Exception as e:
        print(f'❌ Request failed: {e}')

if __name__ == "__main__":
    test_recommendations_only()
