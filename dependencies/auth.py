
from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session

from configs.logger import get_logger
from database.session import get_db
from security.jwt import validate_access_token

logger = get_logger("auth-dependencies")

def current_user(request:Request, db:Session = Depends(get_db)):
    
    try:
        
        access_token = request.cookies.get(
            "access_token"
        )
        
        if access_token is None:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated"
            )
            
        try:
        
            payload = validate_access_token(access_token)
        
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expire token"
            )
            
        user_id_string = payload.get("sub")
        
        if user_id_string is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        
        
        
        
    except Exception:
        logger.exception("Unexpected error in current user")
        raise
        