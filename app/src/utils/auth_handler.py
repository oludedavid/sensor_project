import time
from typing import Dict, Optional

import jwt
import os


JWT_SECRET = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")


def token_response(token: str) -> Dict[str, str]:
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Optional[Dict[str, str]]:
    # Check if required environment variables are set
    if not JWT_SECRET or not JWT_ALGORITHM:
        return None
    
    payload = {
        "user_id": user_id,
        "expires": time.time() + 900
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> Optional[dict]:
    # Check if required environment variables are set
    if not JWT_SECRET or not JWT_ALGORITHM:
        return None
    
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception:
        return None