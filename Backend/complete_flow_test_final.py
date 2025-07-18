"""
Complete Text Flow Test - Fixed with proper timeouts
"""
import requests
import json
import time

def test_complete_text_flow_fixed():
    """Test complete text flow with proper timeouts"""
    
    print("🎯 COMPLETE TEXT FLOW TEST - FINAL VERSION")
    print("=" * 60)
    
    base_url = "http://localhost:8000/api"
    
    # Step 1: Text Prediction
    print("\n1️⃣ Text Prediction...")
    text_data = {
        "waste_type": "I have 1000 kg of cattle manure from my dairy farm",
        "quantity": 1000,
        "location": "Maharashtra"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/predict-text", json=text_data, timeout=20)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS ({elapsed:.2f}s)")
            print(f"   Classified: {result['waste_type']}")
            waste_type = result['waste_type']
            quantity = result['quantity']
        else:
            print(f"❌ FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    # Step 2: Recommendations  
    print("\n2️⃣ Recommendations...")
    rec_data = {
        "waste_type": waste_type,
        "quantity": quantity,
        "location": "Maharashtra"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/recommend", json=rec_data, timeout=20)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS ({elapsed:.2f}s)")
            # Try both field names for compatibility
            processing_method = result.get('processing_method') or result.get('recommended_method')
            print(f"   Method: {processing_method}")
        else:
            print(f"❌ FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    # Step 3: GHG Calculation
    print("\n3️⃣ GHG Calculation...")
    ghg_data = {
        "waste_type": waste_type,
        "quantity": quantity,
        "processing_method": processing_method,
        "location": "Maharashtra"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/ghg-savings", json=ghg_data, timeout=20)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS ({elapsed:.2f}s)")
            print(f"   CO2 Saved: {result['co2_saved']} {result.get('co2_saved_unit', 'kg')}")
            co2_saved = result['co2_saved']
        else:
            print(f"❌ FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    # Step 4: Carbon Credits
    print("\n4️⃣ Carbon Credits...")
    credit_data = {
        "co2_saved": co2_saved,
        "waste_type": waste_type,
        "processing_method": processing_method,
        "verification_level": "standard"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/carbon-credit", json=credit_data, timeout=20)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS ({elapsed:.2f}s)")
            print(f"   Credits: {result['credits_earned']:.2f} {result.get('credits_unit', 'tCO2e')}")
            print(f"   Value: ₹{result['market_value']:.2f}")
            carbon_credits = result['credits_earned']
        else:
            print(f"❌ FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    # Step 5: Certificate Generation
    print("\n5️⃣ Certificate Generation...")
    cert_data = {
        "analysis_id": "test-complete-flow",
        "user_name": "Test User",
        "waste_type": waste_type,
        "co2_saved": co2_saved,
        "carbon_credits": carbon_credits,
        "processing_method": processing_method
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/generate-certificate", json=cert_data, timeout=20)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✅ SUCCESS ({elapsed:.2f}s)")
            print(f"   PDF Size: {len(response.content):,} bytes")
            
            # Save certificate for verification
            with open("complete_flow_certificate.pdf", "wb") as f:
                f.write(response.content)
            print("   📄 Certificate saved as: complete_flow_certificate.pdf")
        else:
            print(f"❌ FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 COMPLETE TEXT FLOW TEST: 100% SUCCESS!")
    print("🚀 TEXT INPUT FUNCTIONALITY IS FULLY WORKING!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_complete_text_flow_fixed()
    if success:
        print("\n✅ ALL SYSTEMS OPERATIONAL - READY FOR PRODUCTION!")
    else:
        print("\n❌ SOME ISSUES FOUND - CHECK LOGS ABOVE")
