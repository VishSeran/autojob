from datetime import datetime
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import select

from configs.logger import get_logger
from models.user_session import UserSession

logger = get_logger("user-session")

class UserSessionRepository:
    
    def __init__(self, db:Session):
        
        self.db = db
        
        
    def create_sesssion(
        self,
        user_id:uuid.UUID,
        hash_refresh_token:str,
        expires_at:datetime
    ) -> UserSession:
        
        try:
            
            new_session = UserSession(
                
                user_id = user_id,
                hashed_refresh_token = hash_refresh_token,
                expires_at = expires_at
            )
            
            self.db.add(
                new_session
            )
            
            self.db.commit()
            self.db.refresh(new_session)
            
            return new_session
            
        except Exception:
            logger.exception("Unexpected error in create session")
            raise
        
        
    def get_by_hash_refresh_token(self, token_hash:str) -> UserSession | None:
        
        try:
            
            stmt = (
                select(UserSession).where(UserSession.hashed_refresh_token == token_hash)
            )
            
            return self.db.scalar(stmt)
            
        except Exception:
            logger.exception("Unexpected error in get by hash refresh token")
            raise
        
        
    def revoke_session(self, session:UserSession):
        
        try:
            
            session.revoke = True
            self.db.commit()
            self.db.refresh(session)
            
        except Exception:
            self.db.rollback()
            logger.exception("Unexpected error in revoke session")
            raise
                    
        