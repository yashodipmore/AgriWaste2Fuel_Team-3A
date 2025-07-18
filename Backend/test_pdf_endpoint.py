"""
Test the updated PDF certificate generation endpoint
"""
import requests

def test_pdf_certificate_endpoint():
    """Test the complete PDF certificate generation via API endpoint"""
    
    # Test certificate data
    certificate_data = {
        'analysis_id': 'test-pdf-123',
        'user_name': 'Test User PDF',
        'waste_type': 'CATTLE MANURE',
        'co2_saved': 1250.75,
        'carbon_credits': 4.5,
        'processing_method': 'Anaerobic Digestion'
    }
    
    print("Testing PDF certificate generation via API...")
    print(f"Request data: {certificate_data}")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/generate-certificate',
            json=certificate_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f'\nStatus Code: {response.status_code}')
        print(f'Content Type: {response.headers.get("Content-Type")}')
        print(f'Content Length: {len(response.content)} bytes')
        print(f'Content Disposition: {response.headers.get("Content-Disposition")}')
        
        if response.status_code == 200:
            print('✅ PDF Certificate generated successfully!')
            
            # Save the PDF content to file for testing
            with open('api_test_certificate.pdf', 'wb') as f:
                f.write(response.content)
            print('📄 Certificate saved as api_test_certificate.pdf')
            
            # Verify it's a valid PDF
            if response.content.startswith(b'%PDF'):
                print('✅ Valid PDF format confirmed!')
            else:
                print('❌ Invalid PDF format!')
            
        else:
            print(f'❌ Error Response: {response.text}')
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend server not running on localhost:8000")
    except Exception as e:
        print(f'❌ Request failed: {e}')

if __name__ == "__main__":
    test_pdf_certificate_endpoint()
