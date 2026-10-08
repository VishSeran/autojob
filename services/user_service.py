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
            
            
            exisitng_user = self.user_repository.get_by_email(email)
            
            if exisitng_user:
                logger.warning(
                    f"A user with this email already exists: {email}"
                )
                raise ValueError(
                    f"A user with this email already exists: {email}"
                )
                
            new_user = self.user_repository.create(email, name)
            logger.info(f"New user created:{name} - {email}")
                            
            return new_user
    
        except ValueError:
            logger.exception("Unexpected value error in create user")
            raise    
        
        except Exception:
            logger.exception("Unexpected error in create user")
            raise
        
    
    def get_user_by_email(self, email) -> User | str:
        
        try:
            
            user = self.user_repository.get_by_email(email)
            
            if not user:
                logger.warning(f"{email} - user not found")
                return f"{email} - user not found"
                
            return user
        
        except Exception:
            logger.exception("Unexpected error in get user by email")
            raise    
        
        
    