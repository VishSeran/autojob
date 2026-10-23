
import uuid

import resend
from resend.exceptions import ResendError
from sqlalchemy.orm import Session

from configs.logger import get_logger
from configs.settings import settings
from models.gmail import GmailModel
from repositories.gmail_repository import GmailRepository
from repositories.user_repository import UserRepository

logger = get_logger("gmail-service")

class GmailService:
    
    def __init__(self, db:Session):
        
        self.gmail_repository = GmailRepository(db)
        self.user_repository = UserRepository(db)
        logger.info("Gmail service has initialized")
        
        
    async def send_email(
        self, 
        user_id:uuid.UUID,
        company_mail:str,
        subject:str,
        email_body:str
    ) -> GmailModel:
        
        try:
            
            if user_id is None:
                raise ValueError("User ID is missing")
            
            if company_mail is None:
                raise ValueError("Company email is missing")
            
            if subject is None:
                raise ValueError("Email subject is missing")
            
            if email_body is None:
                raise ValueError("Email body is missing")
            
            user = self.user_repository.get_by_id(user_id)
            
            email_data = GmailModel(                    
                user_id= user_id,
                reply_email= user.email,
                company_mail= company_mail,
                subject= subject,
                email_body= email_body,
            )
            
            email_data = self.gmail_repository.create_gmail(email_data)
            logger.info("Send email added to database successfully - pending")
            
            resend.api_key = settings.RESEND_API
            
            params:resend.Emails.SendParams = {
                
                "from": "Acme <onboarding@resend.dev>",
                "to": [company_mail, reply_email],
                "reply_to":reply_email,
                "subject":subject,
                "text":email_body
                
            }
            
            try:
            
                send_email = await resend.Emails.send_async(params)
                logger.info("Email sent successfully")
                
            except ResendError:
                email_data.status = "failed"
                self.gmail_repository.update(email_data)
                logger.exception("Resend failed to send the email")
                raise
            
            resend_email_id = send_email.get("id")
            
            logger.info(
                f"Email accepted by Resend. Resend ID: {resend_email_id}"
            )
            
            email_data.resend_email_id = resend_email_id
            email_data.status = "sent"
            
            self.gmail_repository.update(email_data)
            logger.info(f"Send email added to database successfully - sent: {email_data.id}")
            
            return email_data
    
        except ValueError:
            email_data.status = "failed"
            self.gmail_repository.update(email_data)
            logger.exception("Unexpected value error in send email")
            raise    
            
        except Exception:
            logger.exception("Unexpected error in send email")
            raise
        
        
    def view_all_emails(self, user_id:uuid.UUID):
        
        try:
            
            if user_id is None:
                raise ValueError("User ID is missing")
            
            emails = self.gmail_repository.get_by_user_id(
                user_id
            )
            
            logger.info("Emails are fetched")
            
            return emails
        
        except Exception:
            logger.exception("Unexpected error in view all emails")
            raise
        
        
    def view_email(self, user_id:uuid.UUID, email_id:uuid.UUID):
        
        try:
            
            if user_id is None:
                raise ValueError("User ID is missing")
            
            if email_id is None:
                raise ValueError("Email ID is missing")
            
            email = self.gmail_repository.get_by_id(
                user_id,
                email_id
            )
            
            logger.info('Email is fetched')
            
            return email
            
        except Exception:
            logger.exception("Unexpected error in view email")
            raise
        
        