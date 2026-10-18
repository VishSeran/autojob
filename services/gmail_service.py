
import uuid

from sqlalchemy.orm import Session

from configs.logger import get_logger
from models.gmail import GmailModel
from repositories.gmail_repository import GmailRepository
from repositories.user_repository import UserRepository


logger = get_logger("gmail-service")

class GmailService:
    
    def __init__(self, db:Session):
        
        self.gmail_repository = GmailRepository(db)
        self.user_repository = UserRepository(db)
        logger.info("Gmail service has initialized")
        
        
    def send_email(
        self, 
        user_id:uuid.UUID,
        resend_email_id:str,
        company_mail:str,
        subject:str,
        email_body:str
    )->GmailModel:
        
        try:
            
            
        except Exception:
            logger.exception("Unexpected error in send email")
            raise
        
        