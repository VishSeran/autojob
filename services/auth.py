from sqlalchemy.orm import Session

from configs.logger import get_logger
from repositories.user_repository import UserRepository
from repositories.user_session_repository import UserSessionRepository

logger = get_logger("auth-service")

class AuthService:
    
    def __init__(self, db:Session):
        
        self.user_repository = UserRepository(db)
        self.session_repository =  UserSessionRepository(db)
        
        
    def signup(self, email:str, name:str, password:str):
        
        try:
            
            exisitng_user = self.user_repository.get_by_email(email)
            
            if exisitng_user:
                raise ValueError("Email already registered!!!")
            
            
        
        except ValueError:
            logger.exception("Unexpected value error in signup")
            raise
        
        except Exception:
            logger.info("Unexpected error in signup")
            raise
        
    