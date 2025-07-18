"""
Main API router that includes all endpoint modules
"""

from fastapi import APIRouter

# Import all endpoint modules
from .endpoints import (
    auth,
    predict_image,
    text_prediction,
    recommendations,
    ghg_calculation,
    carbon_credits,
    certificates,
    dashboard
)

# Create main API router
api_router = APIRouter()

# Test endpoint for Part 1
@api_router.get("/test")
async def test_endpoint():
    """
    Test endpoint to verify API is working
    """
    return {
        "message": "AgriWaste2Fuel API is working! 🚀",
        "status": "success",
        "part": "Part 1 - Project Setup Complete"
    }

# Include all route modules with correct paths for frontend
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(predict_image.router, tags=["Image Processing"])
api_router.include_router(text_prediction.router, tags=["Text Processing"])
api_router.include_router(recommendations.router, tags=["Recommendations"])
api_router.include_router(ghg_calculation.router, tags=["GHG Calculations"])
api_router.include_router(carbon_credits.router, tags=["Carbon Credits"])
api_router.include_router(certificates.router, tags=["Certificates"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
