
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import select

from configs.logger import get_logger
from models.gmail import GmailModel


logger = get_logger("gmail-repository")

class GmailRepository:
    
    def __init__(self, db:Session):
        self.db = db
        
        
    def create_gmail(self, gmail:GmailModel) -> GmailModel:
        
        try:
            
            self.db.add(gmail)
            self.db.commit()
            self.db.refresh(gmail)

            logger.info(f"new gmail added: {gmail.id}")
            return gmail
            
        except Exception:
            logger.exception("Unexpected error in create gmail")
            raise
        
    def get_by_id(self, user_id: uuid.UUID, email_id:uuid.UUID) -> GmailModel | None:
        
        try:
            
            stmt = (
                
                select(GmailModel).where(
                    GmailModel.id == email_id,
                    GmailModel.user_id == user_id
                )
            )
            
            email =  self.db.scalar(stmt)
            logger.info("Email fetched")
            
            return email
            
        except Exception:
            logger.exception("Unexpected error in get by id")
            raise
        
        