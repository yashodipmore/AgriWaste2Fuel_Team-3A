#!/usr/bin/env python3
"""
ML Integration Test Script
Tests all ML components for AgriWaste2Fuel system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ml_integration():
    print('🧪 Testing ML Integration Setup...')
    print()

    # Test imports
    try:
        from app.services.ml.image_classifier import WasteImageClassifier
        print('✅ Image classifier import successful')
    except Exception as e:
        print(f'❌ Image classifier import failed: {e}')

    try:
        from app.services.ml.text_classifier import WasteTextClassifier
        print('✅ Text classifier import successful')
    except Exception as e:
        print(f'❌ Text classifier import failed: {e}')

    try:
        from app.services.ml.recommendation_system import get_waste_recommendations
        print('✅ Recommendation system import successful')
    except Exception as e:
        print(f'❌ Recommendation system import failed: {e}')

    try:
        from app.services.ml.model_utils import ModelManager
        print('✅ Model utilities import successful')
    except Exception as e:
        print(f'❌ Model utilities import failed: {e}')

    print()
    print('🔧 Testing ML classifier initialization...')

    # Test text classifier
    try:
        text_classifier = WasteTextClassifier()
        result = text_classifier.predict('rice straw 100kg')
        print(f'✅ Text classifier working: {result["waste_type"]} ({result["confidence"]}%)')
    except Exception as e:
        print(f'❌ Text classifier failed: {e}')

    # Test recommendation system
    try:
        recommendations = get_waste_recommendations('Rice Straw', 1000, 'Maharashtra')
        print(f'✅ Recommendation system working: {len(recommendations)} recommendations')
    except Exception as e:
        print(f'❌ Recommendation system failed: {e}')

    # Test image classifier (without actual model file)
    try:
        image_classifier = WasteImageClassifier()
        print('✅ Image classifier initialized (model loading will be tested separately)')
    except Exception as e:
        print(f'❌ Image classifier initialization failed: {e}')

    print()
    print('🏁 ML Integration setup test complete!')

if __name__ == "__main__":
    test_ml_integration()
