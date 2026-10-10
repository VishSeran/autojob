import uuid
from datetime import datetime, timedelta, timezone

import jwt
from jwt import InvalidTokenError

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
    
    
def validate_access_token(token: str) -> dict:
    
    try:
        
        if not token:
            raise ValueError('Token is missing')
        
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ]
        )
        
        if payload.get("type") != "access":
            
            raise ValueError(
                "Invalid token type"
            )
            
        return payload
        
    except InvalidTokenError:
        raise ValueError(
            "Invalid or expire token access"
        )
    
    except ValueError:
        logger.exception("Unexpected value error in validate access token")
        raise
    
    except Exception:
        logger.exception("Unexpected error in validate access token")
        raise