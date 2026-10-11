from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from configs.logger import get_logger
from configs.settings import settings
from models.users import User
from repositories.user_repository import UserRepository
from repositories.user_session_repository import UserSessionRepository
from security.hashing import hash_password, verify_hash_password
from security.jwt import (
    create_access_token,
    generate_jwt_refresh_token,
    hash_refresh_token,
)

logger = get_logger("auth-service")

class AuthService:
    
    def __init__(self, db:Session):
        
        self.user_repository = UserRepository(db)
        self.session_repository =  UserSessionRepository(db)
        
        
    def signup(self, email:str, name:str, password:str) -> User:
        
        try:
            
            exisitng_user = self.user_repository.get_by_email(email)
            
            if exisitng_user:
                raise ValueError("Email already registered")
            
            name = name.strip()
            hashed_password = hash_password(password)
            
            
            new_user = self.user_repository.create(
                email=email,
                hashed_password=hashed_password,
                name=name
            )
            
            logger.info(f"New use has created: {email}")
            return new_user
            
        except ValueError:
            logger.exception("Unexpected value error in signup")
            raise
        
        except Exception:
            logger.info("Unexpected error in signup")
            raise
        
    
    def login(self, email:str, password:str):
        
        try:
            
            exisitng_user = self.user_repository.get_by_email(email)
            
            if exisitng_user is None:
                raise ValueError("Email is not registered")
            
            is_pass_verified = verify_hash_password(
                password,
                exisitng_user.hashed_password
            )
            
            if not is_pass_verified:
                raise ValueError("Invalid email or password")
            
            
            access_token = (
                create_access_token(exisitng_user.id)
            )
            
            refresh_token = (
                generate_jwt_refresh_token()
            )
            
            refresh_hashed_token = (
                hash_refresh_token(refresh_token)   
            )
            
            expires_at = datetime.now(timezone.utc) + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
            
            new_session = self.session_repository.create_sesssion(
                user_id= exisitng_user.id,
                hash_refresh_token=refresh_hashed_token,
                expires_at=expires_at
            )
            
            logger.info(f"New session has created: {exisitng_user.id}")
            
            return {
                "user": exisitng_user,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
           
        except ValueError:
            logger.exception("Unexpected value error in signup")
            raise
        
        except Exception:
            logger.info("Unexpected error in signup")
            raise