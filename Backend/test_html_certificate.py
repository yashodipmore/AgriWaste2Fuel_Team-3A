"""
Test the updated certificate generation that returns HTML directly
"""
import requests

def test_direct_html_certificate():
    """Test certificate generation that returns HTML content directly"""
    
    # Test certificate data
    certificate_data = {
        'analysis_id': 'test-html-123',
        'user_name': 'Test User HTML',
        'waste_type': 'CATTLE MANURE',
        'co2_saved': 1250.75,
        'carbon_credits': 4.5,
        'processing_method': 'Anaerobic Digestion'
    }
    
    print("Testing direct HTML certificate generation...")
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
            print('✅ Certificate HTML generated successfully!')
            
            # Save the HTML content to file for testing
            with open('test_certificate.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print('📄 Certificate saved as test_certificate.html')
            
            # Show first 200 characters of HTML
            print(f'\nHTML Preview: {response.text[:200]}...')
            
        else:
            print(f'❌ Error Response: {response.text}')
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend server not running on localhost:8000")
    except Exception as e:
        print(f'❌ Request failed: {e}')

if __name__ == "__main__":
    test_direct_html_certificate()
