"""
Authentication endpoints for Firebase integration
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import datetime
from typing import Optional

from app.core.firebase_auth import get_current_user, get_optional_user
from app.models.schemas import BaseResponse

router = APIRouter()

class UserProfileResponse(BaseResponse):
    """User profile response model"""
    uid: str
    email: str
    name: str
    email_verified: bool

class AuthStatusResponse(BaseResponse):
    """Authentication status response"""
    authenticated: bool
    user: Optional[dict] = None

@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user profile
    Requires Firebase authentication token
    """
    return UserProfileResponse(
        uid=current_user["uid"],
        email=current_user["email"], 
        name=current_user["name"],
        email_verified=current_user.get("email_verified", False),
        message=f"Profile retrieved for {current_user['name']}",
        timestamp=datetime.now()
    )

@router.get("/status", response_model=AuthStatusResponse)
async def get_auth_status(user: Optional[dict] = Depends(get_optional_user)):
    """
    Check authentication status
    Works for both authenticated and anonymous users
    """
    if user:
        return AuthStatusResponse(
            authenticated=True,
            user={
                "uid": user["uid"],
                "email": user["email"],
                "name": user["name"]
            },
            message="User is authenticated",
            timestamp=datetime.now()
        )
    else:
        return AuthStatusResponse(
            authenticated=False,
            user=None,
            message="User is not authenticated",
            timestamp=datetime.now()
        )

@router.post("/verify-token")
async def verify_token(current_user: dict = Depends(get_current_user)):
    """
    Verify Firebase token validity
    Returns user info if token is valid
    """
    return {
        "valid": True,
        "user": {
            "uid": current_user["uid"],
            "email": current_user["email"],
            "name": current_user["name"],
            "email_verified": current_user.get("email_verified", False)
        },
        "message": "Token is valid",
        "timestamp": datetime.now()
    }

@router.delete("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout endpoint (client-side token invalidation)
    Firebase tokens are stateless, so logout is handled on frontend
    """
    return {
        "success": True,
        "message": f"User {current_user['name']} logged out successfully",
        "note": "Firebase tokens are stateless. Clear token on frontend.",
        "timestamp": datetime.now()
    }
