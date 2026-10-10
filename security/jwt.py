import uuid
from datetime import datetime, timedelta, timezone

import jwt

from configs.logger import get_logger
from configs.settings import settings

logger = get_logger("jwt")

def create_access_token(user_id: uuid.UUID) -> str:
    
    try:
    
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
    
    except ValueError:
        logger.exception("Unecpected value error in create access token")
        raise
    
    except Exception:
        logger.exception("Unecpected error in create access token")
        raise