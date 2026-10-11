from sqlalchemy.orm import Session
from repositories.user_session_repository import UserSessionRepository
from configs.logger import get_logger


logger = get_logger("user-session-service")

class UserSessionService:
    
    def __init__(self, db:Session):
        
        self.session_repository =  UserSessionRepository(db)
        
    def create_session(self, )