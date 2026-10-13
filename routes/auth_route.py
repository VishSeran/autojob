from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from configs.logger import get_logger
from database.session import get_db
from schema.auth import LogInRequest, LogInResponse, SignUpRequest, UserResponse
from services.auth_service import AuthService

logger = get_logger("auth-route")

auth_router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@auth_router.post("/signup", response_model=UserResponse,status_code=201)
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
        
        logger.info(f"User {new_user.id} has created")
        return new_user
    
    except ValueError as error:
        logger.error(f"Unexpected value error in signup: {error}")
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )


@auth_router.post("/login", response_model=LogInResponse)
def login(data:LogInRequest, response:Response, db:Session = Depends(get_db)):
    
        
    if data is None:
        raise ValueError("Requested data is missing")
    
    auth_service = AuthService(db)
        
    try:
            login_response = auth_service.login(
                email=data.email,
                password=data.password
            )
            
            logger.info("User login response has received")
            
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
            
            logger.info("Access token has set to cookies")
            
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age= 30*24*60*60
            )
            
            logger.info("Refresh token has set to cookies")
            
            return {
                "message": "Logged in Successfully",
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


@auth_router.post("/logout")
def logout(request:Request, response: Response, db:Session = Depends(get_db)):
    
    try:
        
        refresh_token = request.cookies.get("refresh_token")
        logger.info("Got the refresh token")
        
        if refresh_token:
            auth_service = AuthService(db)
            auth_service.logout(refresh_token)
            
        response.delete_cookie(
            "access_token",
            path="/",
        )
        logger.info("Access token has deleted from cookies")
        
        response.delete_cookie(
            "refresh_token",
            path="/",
        )
        logger.info("Refresh token has deleted from cookies")
 
        return {
            
            "message": "Logged out successfully"
        }
     
    except ValueError as error:
        logger.error(f"Unexpected value error in login: {error}")
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )
        
        
@auth_router.get("/refresh")
def refresh(request:Request, response:Response, db:Session = Depends(get_db)):
    
        auth_service = AuthService(db)
        
        try:
        
            refresh_token = request.cookies.get(
                "refresh_token"
            )
            
            if refresh_token is None:

                raise HTTPException(
                    status_code=401,
                    detail="Refresh token missing"
                )
            
            new_access_token = auth_service.refresh_access_token(
                refresh_token
            )
            logger.info("New access token has created")
            
            response.set_cookie(
                "access_token",
                new_access_token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age= 30 * 60
            )
            logger.info('Cookies has updated')
            
            return {
                
                "message": "access token refreshed"
            }
            
        except ValueError as error:
            raise HTTPException(
                status_code=401,
                detail=str(error)
            )
        

