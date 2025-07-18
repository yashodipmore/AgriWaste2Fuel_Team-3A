"""
Test complete text input flow for AgriWaste2Fuel
"""
import requests
import json

def test_complete_text_flow():
    """Test the complete text input analysis flow"""
    
    # Test data for text input (using correct field name)
    text_data = {
        "waste_type": "I have 1000 kg of cattle manure from my dairy farm",  # Fixed field name
        "quantity": 1000,
        "location": "Maharashtra"
    }
    
    print("🧪 Testing Complete Text Input Flow")
    print("=" * 50)
    
    try:
        # Step 1: Text Prediction
        print("\n1️⃣ Testing Text Prediction...")
        text_response = requests.post(
            'http://localhost:8000/api/predict-text',
            json=text_data,
            headers={'Content-Type': 'application/json'},
            timeout=15  # Increased timeout
        )
        print(f"   Status: {text_response.status_code}")
        
        if text_response.status_code != 200:
            print(f"❌ Text prediction failed: {text_response.text}")
            return
        
        text_result = text_response.json()
        print(f"   ✅ Waste Type: {text_result.get('waste_type')}")
        print(f"   ✅ Quantity: {text_result.get('quantity')} kg")
        
        # Step 2: Recommendations
        print("\n2️⃣ Testing Recommendations...")
        recommend_data = {
            "waste_type": text_result.get('waste_type'),
            "quantity": text_result.get('quantity'),
            "location": "Maharashtra"
        }
        
        recommend_response = requests.post(
            'http://localhost:8000/api/recommend',
            json=recommend_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"   Status: {recommend_response.status_code}")
        
        if recommend_response.status_code != 200:
            print(f"❌ Recommendations failed: {recommend_response.text}")
            return
        
        recommend_result = recommend_response.json()
        print(f"   ✅ Method: {recommend_result.get('recommended_method')}")
        
        # Step 3: GHG Savings
        print("\n3️⃣ Testing GHG Savings...")
        ghg_data = {
            "waste_type": text_result.get('waste_type'),
            "quantity": text_result.get('quantity'),
            "processing_method": recommend_result.get('recommended_method'),
            "location": "Maharashtra"
        }
        
        ghg_response = requests.post(
            'http://localhost:8000/api/ghg-savings',
            json=ghg_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"   Status: {ghg_response.status_code}")
        
        if ghg_response.status_code != 200:
            print(f"❌ GHG savings failed: {ghg_response.text}")
            return
        
        ghg_result = ghg_response.json()
        print(f"   ✅ CO2 Saved: {ghg_result.get('total_co2_saved')} kg")
        
        # Step 4: Carbon Credits (The missing step!)
        print("\n4️⃣ Testing Carbon Credits...")
        carbon_data = {
            "co2_saved": ghg_result.get('total_co2_saved'),
            "waste_type": text_result.get('waste_type'),
            "processing_method": recommend_result.get('recommended_method'),
            "verification_level": "standard"
        }
        
        carbon_response = requests.post(
            'http://localhost:8000/api/carbon-credit',
            json=carbon_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"   Status: {carbon_response.status_code}")
        
        if carbon_response.status_code != 200:
            print(f"❌ Carbon credits failed: {carbon_response.text}")
            return
        
        carbon_result = carbon_response.json()
        print(f"   ✅ Credits: {carbon_result.get('credits_earned')} tCO₂e")
        print(f"   ✅ Value: {carbon_result.get('market_value')}")
        
        # Summary
        print("\n🎉 COMPLETE FLOW SUCCESS!")
        print("=" * 30)
        print(f"Final Results:")
        print(f"• Waste Type: {text_result.get('waste_type')}")
        print(f"• Quantity: {text_result.get('quantity')} kg")
        print(f"• Method: {recommend_result.get('recommended_method')}")
        print(f"• CO2 Saved: {ghg_result.get('total_co2_saved')} kg")
        print(f"• Carbon Credits: {carbon_result.get('credits_earned')} tCO₂e")
        print(f"• Market Value: {carbon_result.get('market_value')}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend server not running")
    except Exception as e:
        print(f'❌ Test failed: {e}')

if __name__ == "__main__":
    test_complete_text_flow()
