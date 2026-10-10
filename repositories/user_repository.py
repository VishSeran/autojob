from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from configs.logger import get_logger
from models.users import User

logger = get_logger("user-repo")

class UserRepository:
    
    def __init__(self, db:Session):
        
        self.db = db
        
    def create(self, email: str, hashed_password: str, name:str | None = None) -> User:
        
        try:
            
            if not email:
                raise ValueError("Email cannot be empty")
            
            new_user = User(
                email = email,
                name=name,
                hashed_password=hashed_password
            )
            
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            
            return new_user
        
        except ValueError:
            logger.exception("Unexpected value error in create user")
            raise
            
        except Exception:
            logger.exception("Unexpected error in create user")
            raise
            
            
    def get_by_email(self, email) -> User | None:
        
        try:
            
            if not email:
                raise ValueError("Email cannot be empty")
            
            # stmt means statement.
            # It is basically a SQLAlchemy object representing the query.
            # So stmt is like a prepared instruction.
            stmt = (
                select(User).where(
                    User.email == email
                )
            )
            
            # This does NOT execute the database query yet.So stmt is like a prepared instruction.
            # This is where the query actually gets executed:
            user = self.db.scalar(stmt)
            
            return user
            
            
        except ValueError:
            logger.exception("Unexpected value error in get by email")
            raise
            
        except Exception:
            logger.exception("Unexpected error in get by email")
            raise
        
        
    def get_by_id(self, user_id) -> User | None:
        
        try:
            
            if not user_id:
                raise ValueError("User Id cannot be empty")
            
            stmt = (
                select(User).where(User.id == user_id)
            )
            
            user = self.db.scalar(stmt)
            return user
            
        except ValueError:
            logger.exception("Unexpected value error in get by id")
            raise
            
        except Exception:
            logger.exception("Unexpected error in get by id")
            raise
        
    def update_name(self, name:str , user: User) -> User:
        
        try:
            
            if not name:
                raise ValueError("Name cannot be empty")
            
            user.name = name
            self.db.commit()
            self.db.refresh(user)
            
            return user
            
        except ValueError:
            logger.exception("Unexpected value error in update name")
            raise
            
        except Exception:
            self.db.rollback()
            logger.exception("Unexpected error in update name")
            raise
        
        
    def delete_user(self, user:User):
        
        
        try:
            
            if not user:
                raise ValueError("User cannot be empty")
            
            self.db.delete(user)
            self.db.commit()
            
            return user
            
            
        except ValueError:
            logger.exception("Unexpected value error in delete user")
            raise
            
        except Exception:
            
            logger.exception("Unexpected error in delete user")
            raise