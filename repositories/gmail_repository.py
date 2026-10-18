
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from configs.logger import get_logger
from models.gmail import GmailModel

logger = get_logger("gmail-repository")

class GmailRepository:
    
    def __init__(self, db:Session):
        self.db = db
        
        
    def create_gmail(self, email:GmailModel) -> GmailModel:
        
        try:
            
            self.db.add(email)
            self.db.commit()
            self.db.refresh(email)

            logger.info(f"new email added: {email.id}")
            return email
            
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
        
    
    def get_by_user_id(self, user_id:uuid.UUID) -> list[GmailModel] | None:
        
        try:
            
            stmt = (
                select(GmailModel).where(
                    GmailModel.user_id == user_id
                )
            )
            
            emails = self.db.scalars(stmt).all()
            logger.info("Emails are fetched")
            
            return list(emails)
            
        except Exception:
            logger.exception("Unexpected error in get by user id")
            raise
        
    
    def update(self, gmail:GmailModel):
        
        try:
            
            self.db.add(gmail)
            self.db.commit()
            self.db.refresh(gmail)
            
            logger.info("Update gmail successfully")
            
        except Exception:
            logger.exception("Unexpected error in update gmail")
            raise   
        
        
    def delete(self, email:GmailModel):
        
        try:
            self.db.delete(email)
            self.db.commit()
            logger.info("Email has deleted successfully")
            
            return email
            
        except Exception:
            self.db.rollback()
            logger.exception("Unexpected error in delete email")
            raise
        
        