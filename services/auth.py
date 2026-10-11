from sqlalchemy.orm import Session

from configs.logger import get_logger
from repositories.user_repository import UserRepository
from repositories.user_session_repository import UserSessionRepository

logger = get_logger("auth-service")

class AuthService:
    
    def __init__(self, db:Session):
        
        self.user_repository = UserRepository(db)
        self.session_repository =  UserSessionRepository(db)
        
    