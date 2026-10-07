

from configs.logger import get_logger
from models.users import User

logger = get_logger("user-repo")

class UserRepository:
    
    def __init__(self, db):
        
        self.db = db
        
    def create_user(self, email: str, name:str | None = None) -> User:
        
        try:
            
            
        except Exception:
            