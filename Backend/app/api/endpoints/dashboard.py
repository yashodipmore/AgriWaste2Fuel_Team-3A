"""
Dashboard endpoints for user statistics and recent activity
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.services.auth_service import get_current_user
from app.models.schemas import UserModel
from app.services.analysis_storage import analysis_storage

router = APIRouter()

class SaveAnalysisRequest(BaseModel):
    """Request model for saving analysis results"""
    waste_type: str
    quantity: float
    confidence: float
    method: str  # "image" or "text"
    co2_saved: float
    carbon_credits: float
    processing_method: str
    location: str = "Unknown"

@router.post("/save-analysis")
async def save_analysis_result(
    request: SaveAnalysisRequest,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Save user's analysis result to history
    """
    try:
        analysis_data = {
            "waste_type": request.waste_type,
            "quantity": request.quantity,
            "confidence": request.confidence,
            "method": request.method,
            "co2_saved": request.co2_saved,
            "carbon_credits": request.carbon_credits,
            "processing_method": request.processing_method,
            "location": request.location
        }
        
        # Save analysis result
        analysis_id = analysis_storage.save_analysis_result(current_user.uid, analysis_data)
        
        if analysis_id:
            return {
                "status": "success",
                "message": "Analysis result saved successfully",
                "data": {
                    "analysis_id": analysis_id
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save analysis result")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save analysis: {str(e)}")

@router.get("/stats")
async def get_user_stats(current_user: UserModel = Depends(get_current_user)):
    """
    Get user dashboard statistics
    Returns total analyses, CO2 saved, carbon credits, estimated earnings
    """
    try:
        # Get real user statistics from storage
        user_stats = analysis_storage.get_user_stats(current_user.uid)
        
        return {
            "status": "success",
            "data": {
                "totalAnalyses": user_stats.get("total_analyses", 0),
                "co2Saved": round(user_stats.get("total_co2_saved", 0.0), 2),
                "carbonCredits": round(user_stats.get("total_carbon_credits", 0.0), 2),
                "estimatedEarnings": round(user_stats.get("estimated_earnings", 0.0), 2),
                "wasteProcessed": round(user_stats.get("total_waste_processed", 0.0), 2)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user statistics: {str(e)}")

@router.get("/activity")
async def get_recent_activity(
    limit: int = 10,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get user's recent activity/analysis history
    """
    try:
        # Get real user activity from storage
        recent_activities = analysis_storage.get_user_recent_activities(current_user.uid, limit)
        
        # Format activities for frontend
        formatted_activities = []
        for activity in recent_activities:
            formatted_activities.append({
                "id": activity["id"],
                "type": f"{activity['method'].title()} Analysis",
                "wasteType": activity["waste_type"],
                "quantity": activity["quantity"],
                "co2Saved": activity["co2_saved"],
                "carbonCredits": activity["carbon_credits"],
                "timestamp": activity["timestamp"],
                "confidence": activity["confidence"]
            })
        
        return {
            "status": "success",
            "data": {
                "activities": formatted_activities
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recent activity: {str(e)}")

@router.get("/summary")
async def get_dashboard_summary(current_user: UserModel = Depends(get_current_user)):
    """
    Get complete dashboard summary (stats + recent activity)
    """
    try:
        # Get both stats and activity in one call for efficiency
        stats_response = await get_user_stats(current_user)
        activity_response = await get_recent_activity(5, current_user)  # Last 5 activities
        
        return {
            "status": "success",
            "data": {
                "stats": stats_response["data"],
                "recentActivity": activity_response["data"]["activities"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard summary: {str(e)}")
