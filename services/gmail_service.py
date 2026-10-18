
import uuid

from sqlalchemy.orm import Session
import resend
from resend.exceptions import ResendError
from configs.logger import get_logger
from models.gmail import GmailModel
from configs.settings import settings
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
    )->resend.Email:
        
        try:
            
            if user_id is None:
                raise ValueError("User ID is missing")
            
            if resend_email_id is None:
                raise ValueError("Resend email is missing")
            
            if company_mail is None:
                raise ValueError("Company email is missing")
            
            if subject is None:
                raise ValueError("Email subject is missing")
            
            if email_body is None:
                raise ValueError("Email body is missing")
            
            resend.api_key = settings.RESEND_API
            
            params:resend.Emails.SendParams = {
                
                "from": "Acme <onboarding@resend.dev>",
                "to": [company_mail, resend_email_id],
                "reply_to":resend_email_id,
                "subject":subject,
                "text":email_body
                
            }
            
            email = resend.Emails.send(params)
        
            
            return email
            
        
        except ResendError:
            logger.exception("Unexpected error in send email")
            raise    
            
        except ValueError:
            logger.exception("Unexpected value error in send email")
            raise    
            
        except Exception:
            logger.exception("Unexpected error in send email")
            raise
        
        