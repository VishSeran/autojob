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
            logger.info("Access token has created")
            
            refresh_token = (
                generate_jwt_refresh_token()
            )
            logger.info("Refresh token has created")
            
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
            
            logger.info(f"New session has created: {new_session.id}")
            logger.info(f"{new_session.user_id} user has logged in successfully")
            
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
        
        
    def logout(self, token):
        
        try:
            
            if not token:
                logger.warning("Token is missing")
                return
            
            token_hash = hash_refresh_token(token)
            logger.info("Got the token hashed")
            session = self.session_repository.get_by_hash_refresh_token(token_hash)
            logger.info(f"Got the session: {session.id}")
            
            if session is None:
                logger.warning("User session not found")
                return
            
            self.session_repository.revoke_session(session)
            logger.info(f"User session of {session.id} is revoked")
            
        except ValueError:
            logger.exception("Unexpected value error in logout")
            raise
        
        except Exception:
            logger.exception("Unexpected error in logout")
            raise
        
        
    def refresh_access_token(self, refresh_token:str):
        
        try:
            
            if refresh_token is None:
                raise ValueError("Refresh token is missing")
            
            hash_token = hash_refresh_token(
                refresh_token
            )
            logger.info("got the token hashed")
            
            current_session = self.session_repository.get_by_hash_refresh_token(
                hash_token
            )
            
            if current_session is None:
                raise ValueError(
                    "Invalid refresh token"
                )

            if current_session.revoke:
                raise ValueError(
                    "Session revoked"
                )
            
            now = datetime.now(timezone.utc)
            
            if current_session.expires_at < now:
                raise ValueError(
                    "Refresh token has expired"
                )
                
            user = self.user_repository.get_by_id(
                current_session.user_id
            )
            
            if user is None:
                raise  ValueError(
                    "User not found"
                )
                
            new_access_token = create_access_token(user.id)
            logger.info("New access token has created")
            return new_access_token

        except ValueError:
            raise logger.exception("Unexpected value error")

        