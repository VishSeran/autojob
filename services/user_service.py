from uuid import UUID

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
        
        
    def get_user_by_id(self, user_id) -> User | None:
            
        try:
            
            user = self.user_repository.get_by_id(user_id)
            
            if not user:
                logger.warning(f"{user_id} - user not found")
                return None
                
            return user
        
        except Exception:
            logger.exception("Unexpected error in get user by email")
            raise   
        
        
    def update_user(self, email:str | None, user_id:UUID | None, name:str) -> User:
        
        try:
            if not name or not name.strip():
                raise ValueError("Name is required")
            
            user = None
            
            if email is None and user_id is None:
                raise ValueError(
                    "Please provide either email or user ID"
                )
                
            if email is not None and user_id is not None:
                raise ValueError(
                    "Please provide either email or user ID, not both"
                )
            
            if email:
                user = self.get_user_by_email(email)
                
            else:
                user = self.get_user_by_id(user_id)
            
            if user is None:
                raise ValueError(
                    "User not found"
                )
            
            updated_user = self.user_repository.update_name(name.strip(), user)
            logger.info("{updated_user.name} - updated")
            
            return updated_user
            
        except ValueError:
            logger.exception(
                "Validation error while updating user"
            )
            raise

        except Exception:
            logger.exception(
                "Unexpected error while updating user"
            )
            raise
        
        
    def delete_user(self, email:str | None, user_id:UUID | None) -> User:
           
        try:

            user = None
            
            if email is None and user_id is None:
                raise ValueError(
                    "Please provide either email or user ID"
                )
                
            if email is not None and user_id is not None:
                raise ValueError(
                    "Please provide either email or user ID, not both"
                )
            
            if email:
                user = self.get_user_by_email(email)
                
            else:
                user = self.get_user_by_id(user_id)
            
            if user is None:
                raise ValueError(
                    "User not found"
                )
            
            deleted_user = self.user_repository.delete_user(user)
            logger.info("{deleted_user.name} - deleted")
            
            return deleted_user
            
        except ValueError:
            logger.exception(
                "Validation error while deteling user"
            )
            raise

        except Exception:
            logger.exception(
                "Unexpected error while deleting user"
            )
            raise 
    
            