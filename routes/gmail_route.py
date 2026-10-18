
from fastapi import APIRouter, Response, Depends

from configs.logger import get_logger
from database.session import get_db
from dependencies.auth import get_current_user
from models.users import User
from schema.gmail_schema import GmailRequest
from sqlalchemy.orm import Session

from services.gmail_service import GmailService


logger = get_logger("gmail-router")

gmail_router = APIRouter(
    prefix="/gmail",
    tags=["gmail"]
)


@gmail_router.post("/send")
def send_mail(request: GmailRequest, 
              response:Response,
              db:Session = Depends(get_db),
              current_user:User = Depends(get_current_user)):
    
    
    user_id = current_user.id
    logger.info(f"User ID is exctracted: {user_id}")
    
    gmail_service = GmailService(db)
    
    sent_mail = gmail_service.send_email(
        user_id= user_id,
        reply_email= request.reply_email,
        company_mail= request.company_mail,
        subject= request.subject,
        email_body= request.email_body
    )
    
    logger.info("Email sent successfully")
    
    return {
        "message": "Email sent successfully",
        "email_id": sent_mail.id
    }
    

