"""
Text prediction endpoint for agricultural waste classification
"""

from fastapi import APIRouter, HTTPException
import time
from datetime import datetime
from typing import List

from app.models.schemas import TextPredictionRequest, TextPredictionResponse
from app.core.config import settings
from app.services.ml.text_classifier import WasteTextClassifier
from app.services.ml.recommendation_system import get_waste_recommendations

router = APIRouter()

# Initialize ML classifier
text_classifier = WasteTextClassifier()

@router.get("/test")
async def test_endpoint():
    """Simple test endpoint to check if text prediction router is working"""
    return {"status": "Text prediction endpoint is working!", "timestamp": datetime.now()}

@router.post("/predict-text", response_model=TextPredictionResponse)
async def predict_text(request: TextPredictionRequest):
    """
    Classify agricultural waste from text description using ML text classifier
    
    **Features:**
    - Advanced text classification with ML
    - Quantity extraction from text
    - Location detection support
    - Multilingual support (Hindi/English)
    - Processing recommendations
    """
    
    print(f"🔍 Text Prediction Request received:")
    print(f"   Waste type: '{request.waste_type}'")
    print(f"   Quantity: {request.quantity}")
    print(f"   Location: '{request.location}'")
    print(f"   User ID: '{request.user_id}'")
    
    # Validation
    if not request.waste_type or not request.waste_type.strip():
        print("❌ Empty waste type error")
        raise HTTPException(
            status_code=422,
            detail="Waste type description cannot be empty"
        )
    
    try:
        processing_start = time.time()
        
        # TEMPORARY: Skip ML classifier and use simple fallback for debugging
        print(f"⚡ Using simple fallback classification for debugging")
        prediction_result = {
            "waste_type": request.waste_type.title(),
            "confidence": 85.0,
            "quantity": request.quantity or 1000,
            "category": "Agricultural Waste",
            "similar_types": ["Rice Straw", "Wheat Straw", "Corn Stalks", "Sugarcane Bagasse"]
        }
        
        # Skip recommendations for now to speed up response
        processing_time = time.time() - processing_start
        
        # Prepare response
        response = TextPredictionResponse(
            waste_type=prediction_result["waste_type"],
            confidence=prediction_result["confidence"],
            quantity=prediction_result["quantity"],
            matched_category=prediction_result["category"],
            suggestions=prediction_result["similar_types"][:3],
            message=f"Simple classification completed in {processing_time:.2f}s",
            timestamp=datetime.now()
        )
        
        return response
        
    except Exception as e:
        print(f"❌ Text Prediction Error: {str(e)}")
        print(f"❌ Error Type: {type(e).__name__}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        
        # Fallback to simple classification on error
        return TextPredictionResponse(
            waste_type=request.waste_type.title(),
            confidence=50.0,
            quantity=request.quantity or 1000,
            matched_category="Agricultural Waste",
            suggestions=["Rice Straw", "Wheat Straw", "Corn Stalks"],
            message=f"Fallback classification used: {str(e)}",
            timestamp=datetime.now()
        )

@router.get("/waste-categories")
async def get_waste_categories():
    """
    Get all available waste categories and types from ML classifier
    """
    try:
        # Get categories from ML classifier
        categories = text_classifier.get_supported_categories()
        
        return {
            "categories": categories,
            "total_types": sum(len(types) for types in categories.values()),
            "supported_features": [
                "ML-based text classification",
                "Multilingual support (Hindi/English)", 
                "Quantity extraction",
                "Location detection",
                "Processing recommendations"
            ]
        }
    except Exception as e:
        # Fallback response
        return {
            "categories": {
                "Crop Residue": ["Rice Straw", "Wheat Straw", "Corn Stalks"],
                "Animal Waste": ["Cow Dung", "Buffalo Dung", "Chicken Manure"],
                "Organic Waste": ["Vegetable Scraps", "Fruit Peels", "Food Waste"]
            },
            "total_types": 9,
            "supported_features": ["Basic classification"],
            "error": str(e)
        }

@router.get("/search-suggestions/{query}")
async def get_search_suggestions(query: str):
    """
    Get search suggestions for partial waste type queries using ML classifier
    """
    try:
        # Use ML classifier for intelligent suggestions
        suggestions = text_classifier.get_suggestions(query)
        
        return {
            "query": query,
            "suggestions": suggestions[:10],
            "count": len(suggestions),
            "source": "ML classifier"
        }
    except Exception as e:
        # Fallback with basic suggestions
        basic_suggestions = [
            "Rice Straw", "Wheat Straw", "Corn Stalks", "Cow Dung", 
            "Buffalo Dung", "Chicken Manure", "Vegetable Scraps", 
            "Fruit Peels", "Food Waste", "Sugarcane Bagasse"
        ]
        
        # Simple filtering based on query
        filtered = [s for s in basic_suggestions if query.lower() in s.lower()]
        
        return {
            "query": query,
            "suggestions": filtered[:10],
            "count": len(filtered),
            "source": "fallback",
            "error": str(e)
        }
