import uuid
from datetime import datetime, timedelta, timezone

import jwt

from configs.settings import settings


def create_access_token(user_id: uuid.UUID) :
    
    if not user_id:
        raise ValueError ("User ID is missing")
    
    now = datetime.now(timezone.utc)
    
    exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINS)
    
    payload = {
        
        "sub": str(user_id),
        "iat": now,
        "exp": exp,
        "type": "access"
    }
    
    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token