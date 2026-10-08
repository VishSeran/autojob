from sqlalchemy.orm import Session

from configs.logger import get_logger
from models.users import User
from repositories.user_repository import UserRepository


logger = get_logger("user-service")

class UserService:
    
    def __init__(self, db: Session):
        
        self.db = db
        self.user_repository = UserRepository(self.db)
        logger.info("user repository created")
        
    
    def create_user(self, email: str, name: str) -> User:
        
        try:
            
            if not email:
                raise ValueError("Email is missing")
            
            if not name:
                raise ValueError("Name is missing")
            
            
            exisitng_user = 
        
        except ValueError:
            logger.exception("Unexpected value error in create user")
            raise    
        
        except Exception:
            logger.exception("Unexpected error in create user")
            raise