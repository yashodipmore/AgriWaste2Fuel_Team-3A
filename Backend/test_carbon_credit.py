"""
Test the carbon credit endpoint
"""
import requests
import json

def test_carbon_credit_endpoint():
    """Test the carbon credit calculation endpoint"""
    
    # Test carbon credit data
    credit_data = {
        'co2_saved': 5.25,
        'waste_type': 'CATTLE MANURE',
        'processing_method': 'Anaerobic Digestion',
        'verification_level': 'standard'
    }
    
    print("Testing carbon credit calculation...")
    print(f"Request data: {json.dumps(credit_data, indent=2)}")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/carbon-credit',
            json=credit_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f'\nStatus Code: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print('✅ Carbon credit calculation successful!')
            print(f"Credits Earned: {result['credits_earned']} {result['credits_unit']}")
            print(f"Market Value: ₹{result['market_value']} {result['currency']}")
            print(f"Market Type: {result['market_info']['market_type']}")
            print(f"Eligibility: {result['eligibility_status']}")
        else:
            print(f'❌ Error Response: {response.text}')
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend server not running on localhost:8000")
    except Exception as e:
        print(f'❌ Request failed: {e}')

if __name__ == "__main__":
    test_carbon_credit_endpoint()
