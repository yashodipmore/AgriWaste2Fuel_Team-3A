"""
Firebase Authentication Integration
"""

import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends, Request
from typing import Optional
import os
import json

# Global Firebase app instance
firebase_app = None

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global firebase_app
    
    if firebase_app is None:
        try:
            # Check if running in development mode
            if os.getenv("ENVIRONMENT") == "development":
                # For development, you can use service account key file
                service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
                if service_account_path and os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_app = firebase_admin.initialize_app(cred, {
                        'projectId': 'agriwaste2fuel-737b5'
                    })
                else:
                    # If no service account file, use default credentials
                    firebase_app = firebase_admin.initialize_app()
            else:
                # For production, use environment variables or default credentials
                firebase_config = os.getenv("FIREBASE_CONFIG")
                if firebase_config:
                    # Parse JSON config from environment variable
                    config_dict = json.loads(firebase_config)
                    cred = credentials.Certificate(config_dict)
                    firebase_app = firebase_admin.initialize_app(cred)
                else:
                    # Use default credentials (for Cloud Run, etc.)
                    firebase_app = firebase_admin.initialize_app()
                    
            print("✅ Firebase initialized successfully")
            return firebase_app
            
        except Exception as e:
            print(f"❌ Firebase initialization failed: {str(e)}")
            # For development, continue without Firebase
            if os.getenv("ENVIRONMENT") == "development":
                print("⚠️ Running in development mode without Firebase")
                return None
            else:
                raise HTTPException(
                    status_code=500, 
                    detail="Firebase authentication not configured"
                )
    
    return firebase_app

def verify_firebase_token(token: str) -> dict:
    """
    Verify Firebase ID token and return user info
    """
    if not firebase_app:
        # For development mode without Firebase
        if os.getenv("ENVIRONMENT") == "development":
            return {
                "uid": "dev_user_123",
                "email": "dev@example.com",
                "name": "Development User"
            }
        else:
            raise HTTPException(status_code=500, detail="Firebase not initialized")
    
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        
        # Extract user information
        user_info = {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name", decoded_token.get("email", "Unknown")),
            "email_verified": decoded_token.get("email_verified", False),
            "firebase_claims": decoded_token
        }
        
        return user_info
        
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Authentication token has expired")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

def get_current_user(request: Request) -> dict:
    """
    Dependency to get current user from Firebase token
    """
    # Get token from Authorization header
    authorization = request.headers.get("Authorization")
    
    if not authorization:
        # For development, allow requests without token
        if os.getenv("ENVIRONMENT") == "development":
            return {
                "uid": "dev_user_123",
                "email": "dev@example.com", 
                "name": "Development User"
            }
        else:
            raise HTTPException(status_code=401, detail="Authorization header missing")
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    # Verify token and return user info
    return verify_firebase_token(token)

# Optional user dependency (allows both authenticated and anonymous users)
def get_optional_user(request: Request) -> Optional[dict]:
    """
    Dependency to optionally get current user (allows anonymous access)
    """
    try:
        return get_current_user(request)
    except HTTPException:
        return None

# Initialize Firebase on module import
initialize_firebase()
