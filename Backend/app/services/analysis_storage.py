"""
Analysis storage service for saving user analysis results
This provides in-memory storage until database integration
"""

from datetime import datetime
from typing import Dict, List, Optional
import json

# In-memory storage (will be replaced with database)
user_analyses = {}  # user_id: [analysis_results]
user_stats = {}     # user_id: {stats}

class AnalysisStorage:
    @staticmethod
    def save_analysis_result(user_id: str, analysis_data: Dict) -> str:
        """Save analysis result for a user"""
        try:
            if user_id not in user_analyses:
                user_analyses[user_id] = []
            
            # Create analysis record
            analysis_record = {
                "id": f"analysis_{len(user_analyses[user_id]) + 1}_{int(datetime.now().timestamp())}",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "waste_type": analysis_data.get("waste_type", "Unknown"),
                "quantity": analysis_data.get("quantity", 0),
                "confidence": analysis_data.get("confidence", 0),
                "method": analysis_data.get("method", "unknown"),  # image or text
                "co2_saved": analysis_data.get("co2_saved", 0),
                "carbon_credits": analysis_data.get("carbon_credits", 0),
                "processing_method": analysis_data.get("processing_method", "Unknown"),
                "location": analysis_data.get("location", "Unknown")
            }
            
            # Add to user's analysis history
            user_analyses[user_id].append(analysis_record)
            
            # Update user stats
            AnalysisStorage._update_user_stats(user_id, analysis_record)
            
            return analysis_record["id"]
            
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return None
    
    @staticmethod
    def _update_user_stats(user_id: str, analysis_record: Dict):
        """Update user statistics"""
        if user_id not in user_stats:
            user_stats[user_id] = {
                "total_analyses": 0,
                "total_co2_saved": 0.0,
                "total_carbon_credits": 0.0,
                "total_waste_processed": 0.0,
                "estimated_earnings": 0.0
            }
        
        stats = user_stats[user_id]
        stats["total_analyses"] += 1
        stats["total_co2_saved"] += analysis_record.get("co2_saved", 0)
        stats["total_carbon_credits"] += analysis_record.get("carbon_credits", 0)
        stats["total_waste_processed"] += analysis_record.get("quantity", 0)
        
        # Estimate earnings (₹1500 per carbon credit average)
        stats["estimated_earnings"] = stats["total_carbon_credits"] * 1500
    
    @staticmethod
    def get_user_stats(user_id: str) -> Dict:
        """Get user statistics"""
        return user_stats.get(user_id, {
            "total_analyses": 0,
            "total_co2_saved": 0.0,
            "total_carbon_credits": 0.0,
            "total_waste_processed": 0.0,
            "estimated_earnings": 0.0
        })
    
    @staticmethod
    def get_user_recent_activities(user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's recent analysis activities"""
        user_history = user_analyses.get(user_id, [])
        # Return most recent activities (sorted by timestamp)
        sorted_activities = sorted(user_history, key=lambda x: x["timestamp"], reverse=True)
        return sorted_activities[:limit]
    
    @staticmethod
    def get_all_user_analyses(user_id: str) -> List[Dict]:
        """Get all analyses for a user"""
        return user_analyses.get(user_id, [])

# Global instance
analysis_storage = AnalysisStorage()
