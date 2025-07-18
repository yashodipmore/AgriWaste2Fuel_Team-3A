"""
Authentication service for user management
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import logging

from app.models.schemas import UserModel

# Initialize security
security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> UserModel:
    """
    Get current authenticated user
    
    For now, this is a simplified implementation.
    In production, this should validate JWT tokens with Firebase.
    """
    
    try:
        # If no credentials provided, return anonymous user for dashboard access
        if not credentials:
            return UserModel(
                uid="anonymous",
                email="demo@agri.com",
                display_name="Demo User",
                email_verified=True
            )
        
        # In production, validate token with Firebase here
        token = credentials.credentials
        
        # For demo purposes, accept any token
        if token:
            return UserModel(
                uid="demo_user_123",
                email="user@agri.com",
                display_name="Agricultural User",
                email_verified=True
            )
        
        # Return demo user if validation fails
        return UserModel(
            uid="demo",
            email="demo@agri.com", 
            display_name="Demo User",
            email_verified=True
        )
        
    except Exception as e:
        logging.warning(f"Auth validation failed: {e}")
        
        # Return demo user for development
        return UserModel(
            uid="demo",
            email="demo@agri.com",
            display_name="Demo User", 
            email_verified=True
        )

async def verify_token(token: str) -> Optional[UserModel]:
    """
    Verify authentication token
    
    In production, this should integrate with Firebase Auth.
    """
    
    try:
        # Placeholder implementation
        # In production: decode and verify JWT with Firebase
        
        if token and len(token) > 10:
            return UserModel(
                uid="verified_user",
                email="verified@agri.com",
                display_name="Verified User",
                email_verified=True
            )
        
        return None
        
    except Exception as e:
        logging.error(f"Token verification failed: {e}")
        return None

# Optional dependency for routes that don't require auth
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[UserModel]:
    """
    Get current user but don't require authentication
    """
    try:
        return await get_current_user(credentials)
    except:
        return None
