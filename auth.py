import os
from typing import Optional
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

# Optional API key from environment
API_KEY = os.getenv("API_KEY")

# HTTP Bearer security scheme
security = HTTPBearer(auto_error=False)


async def verify_api_key(request: Request, credentials: Optional[HTTPAuthorizationCredentials] = None):
    """
    Verify API key if one is configured.
    If no API key is set in environment, allow all requests.
    """
    # If no API key is configured, allow all requests
    if not API_KEY:
        return True
    
    # Get credentials from Authorization header
    if credentials is None:
        credentials = await security(request)
    
    # Check if credentials were provided
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify the API key
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return True