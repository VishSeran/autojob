from sqlalchemy.orm import Session

from configs.logger import get_logger
from models.users import User
from repositories.user_repository import UserRepository
from repositories.user_session_repository import UserSessionRepository
from security.hashing import hash_password

logger = get_logger("auth-service")

class AuthService:
    
    def __init__(self, db:Session):
        
        self.user_repository = UserRepository(db)
        self.session_repository =  UserSessionRepository(db)
        
        
    def signup(self, email:str, name:str, password:str) -> User:
        
        try:
            
            exisitng_user = self.user_repository.get_by_email(email)
            
            if exisitng_user:
                raise ValueError("Email already registered!!!")
            
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
        
    