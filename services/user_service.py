from sqlalchemy.orm import Session
from uuid import UUID

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
            
            if not email or not email.strip():
                raise ValueError("Email is required")

            if not name or not name.strip():
                raise ValueError("Name is required")

            email = email.strip()
            name = name.strip()
            
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
        
    
    def get_user_by_email(self, email) -> User | None:
        
        try:
            
            user = self.user_repository.get_by_email(email)
            
            if not user:
                logger.warning(f"{email} - user not found")
                return None
                
            return user
        
        except Exception:
            logger.exception("Unexpected error in get user by email")
            raise    
        
        
    def get_user_by_id(self, user_id:UUID) -> User | None:
            
        try:
            
            user = self.user_repository.get_by_id(user_id)
            
            if not user:
                logger.warning(f"{user_id} - user not found")
                return None
                
            return user
        
        except Exception:
            logger.exception("Unexpected error in get user by email")
            raise   
        
        
    def update_user(self, user:User, name) -> User:
        
        try:
            
            updated_user = self.user_repository.update_name(name, user)
            logger.info("{user.name} - updated")
            
            return updated_user
            
        except Exception:
            logger.exception("Unexpected error in get user by email")
            raise  
    
            