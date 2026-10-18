
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
        reply_email:str,
        company_mail:str,
        subject:str,
        email_body:str
    ) -> GmailModel:
        
        try:
            
            if user_id is None:
                raise ValueError("User ID is missing")
            
            if reply_email is None:
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
                "to": [company_mail, reply_email],
                "reply_to":reply_email,
                "subject":subject,
                "text":email_body
                
            }
            
            send_email = resend.Emails.send(params)
            logger.info("Email sent successfully")
            
            resend_email_id = send_email.get("id", "")
            
            email_data = GmailModel(
                            
                user_id= user_id,
                resend_email_id= resend_email_id,
                reply_email= reply_email,
                company_mail= company_mail,
                subject= subject,
                email_body= email_body,
                status="sent"
            )
            
            email_data = self.gmail_repository.create_gmail(email_data)
            logger.info("Send email added to database successfully")
            
            return email_data
            

        except ResendError:            
            logger.exception("Unexpected error in send email")
            raise    
            
        except ValueError:
            logger.exception("Unexpected value error in send email")
            raise    
            
        except Exception:
            logger.exception("Unexpected error in send email")
            raise
        
        