
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from configs.logger import get_logger
from database.session import get_db
from dependencies.auth import get_current_user
from models.users import User
from schema.gmail_schema import GmailRequest
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
    
@gmail_router.get("allmails")
def view_all_mails(request:Request,
                   current_user:User = Depends(get_current_user),
                   db:Session = Depends(get_db)):
    
    user_id = current_user.id
    logger.info(f"User ID is exctracted: {user_id}")
    
    try:
        gmail_service = GmailService(db)
        all_emails =  gmail_service.view_all_emails(user_id)
        logger.info("All emails are retrieved")
    
    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=f"Error in view all emails: {error}"
        )
            
    return {
        
        "message": "All emails are fetched",
        "emails": all_emails,
        "no_emails": str(len(all_emails))
    }


@gmail_router.get("/{gmail_id}")
def view_email(gmail_id:uuid.UUID,
               current_user:User = Depends(get_current_user),
               db:Session = Depends(get_db)):
    
    user_id = current_user.id
    logger.info(f"User ID is exctracted: {user_id}")
    
    try:
    
        email_service = GmailService(db)
        email = email_service.view_email(
            user_id,gmail_id
        )
        logger.info("Email is retrieved")
        
    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=f"Error in view emails: {error}"
        )
    
    return {
        
        "message": f"{email.id} is retrieved successfully",
        "email": email
    }

    
    

