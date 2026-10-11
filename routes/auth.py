from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from configs.logger import get_logger
from schema.auth import SignUpRequest, UserResponse
from services.auth_service import AuthService


logger = get_logger("auth-route")

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/signup", response_model=UserResponse,status_code=201)
def signup(
    data: SignUpRequest,
    db: Session
):
    
    try:
        
        auth_service = AuthService(db)
        
        new_user = auth_service.signup(
            email=data.email,
            name=data.name,
            password=data.password
        )
        
        return new_user
    
    except ValueError as error:
        logger.error(f"Unexpected value error in signup: {e}")
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )
      
    except Exception:
        logger.exception("Unexpected error in signup")
        raise 


