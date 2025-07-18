"""
FastAPI main application for AgriWaste2Fuel Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import routers
from app.api.endpoints import predict_image, text_prediction, dashboard, recommendations, ghg_calculation, certificates

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AgriWaste2Fuel API",
    description="AI-powered agricultural waste management and processing recommendation system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict_image.router, prefix="/api", tags=["Image Prediction"])
app.include_router(text_prediction.router, prefix="/api", tags=["Text Prediction"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])
app.include_router(ghg_calculation.router, prefix="/api", tags=["GHG Calculation"])
app.include_router(certificates.router, prefix="/api", tags=["Certificates"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AgriWaste2Fuel API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "features": [
            "Image-based waste classification",
            "Text-based waste analysis",
            "Processing recommendations",
            "GHG savings calculations"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AgriWaste2Fuel Backend",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
