from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from configs.logger import get_logger
from database.session import get_db
from schema.auth import LogInRequest, LogInResponse, SignUpRequest, UserResponse
from services.auth_service import AuthService

logger = get_logger("auth-route")

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/signup", response_model=UserResponse,status_code=201)
def signup(
    data: SignUpRequest,
    db: Session = Depends(get_db)
):
        
    auth_service = AuthService(db)
    
    try:
    
        new_user = auth_service.signup(
            email=data.email,
            name=data.name,
            password=data.password
        )
        
        return new_user
    
    except ValueError as error:
        logger.error(f"Unexpected value error in signup: {error}")
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )


@router.post("/login", response_model=LogInResponse)
def login(data:LogInRequest, response:Response, db:Session = Depends(get_db)):
    
        
    if data is None:
        raise ValueError("Requested data is missing")
    
    auth_service = AuthService(db)
        
    try:
            login_response = auth_service.login(
                email=data.email,
                password=data.password
            )
            
            access_token = login_response['access_token']
            refresh_token = login_response['refresh_token']
            user = login_response['user']
            
            
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=30*60
            )
            
            response.set_cookie(
                key="resfresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age= 30*24*60*60
            )
            
            logger.info("Cookies are created")

            return {
                "message": "LogIn Successfull",
                "user": {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email
                }
            }
            
    except ValueError as error:
        logger.error(f"Unexpected value error in login: {error}")
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )


@router.post("/logout")
def logout(request:Request , response: Response, db:Session = Depends(get_db)):
    
    try:
        
        refresh_token = request.cookies.get("refresh_token")
        
        if refresh_token:
            auth_service = AuthService(db)
            auth_service.logout(refresh_token)
            
        response.delete_cookie(
            "access_token"
        )
        
        response.delete_cookie(
            "refresh_token"
        )
 
        return {
            "message": "Logged out successfully"
        }
     
    except ValueError as error:
        logger.error(f"Unexpected value error in login: {error}")
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )
        
        

