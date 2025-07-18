"""
Test the JavaScript-like parsing logic for certificate data
"""

def test_parsing():
    """Test parsing strings with units to extract numbers"""
    
    # Test values that might come from frontend
    test_values = [
        '1250.75 kg',
        '4.5 credits', 
        '1250.75',
        4.5,
        '123.45 units CO2',
        '0.75 tonnes',
        'invalid text',
        '',
        None
    ]
    
    print("Testing JavaScript-like parsing logic:")
    print("=" * 50)
    
    for val in test_values:
        try:
            # Mimic JavaScript: String(val).replace(/[^\d.-]/g, '')
            str_val = str(val) if val is not None else ''
            # Remove all characters except digits, dots, and hyphens
            cleaned = ''.join(c for c in str_val if c.isdigit() or c in '.-')
            
            # Convert to float, default to 0 if fails
            parsed = float(cleaned) if cleaned and cleaned != '.' and cleaned != '-' else 0.0
            
            print(f"Original: {repr(val):20} -> Cleaned: {repr(cleaned):10} -> Parsed: {parsed}")
            
        except Exception as e:
            print(f"Original: {repr(val):20} -> ERROR: {e}")

if __name__ == "__main__":
    test_parsing()
