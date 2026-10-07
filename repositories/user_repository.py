from sqlalchemy import select, 
from sqlalchemy.orm import Session

from configs.logger import get_logger
from models.users import User

logger = get_logger("user-repo")

class UserRepository:
    
    def __init__(self, db:Session):
        
        self.db = db
        
    def create(self, email: str, name:str | None = None) -> User:
        
        try:
            
            if not email:
                raise ValueError("Email cannot be empty")
            
            new_user = User(
                email = email,
                name=name
            )
            
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh()
            
            return new_user
        
        except ValueError:
            logger.exception("Unexpected value error in create user")
            raise
            
        except Exception:
            logger.exception("Unexpected error in create user")
            raise
            