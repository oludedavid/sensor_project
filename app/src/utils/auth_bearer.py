from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any

from app.src.utils.auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Dict[str, Any]:
        credentials: Optional[HTTPAuthorizationCredentials] = await super(JWTBearer, self).__call__(request)
        
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
        
        payload = self.verify_jwt(credentials.credentials)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        
        return payload

    def verify_jwt(self, jwtoken: str) -> Optional[Dict[str, Any]]:
        try:
            payload = decodeJWT(jwtoken)
            return payload
        except Exception:
            return None