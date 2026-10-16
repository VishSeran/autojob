
import uuid

from fastapi import APIRouter, Request, Response, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session

from configs.logger import get_logger
from database.session import get_db
from dependencies.auth import get_current_user
from models.users import User
from services.resume_service import ResumeService
from services.resume_storage_service import ResumeStorageService
from database.supabase_client import client


logger = get_logger("resume-route")

MAX_FILE_SIZE = 5 * 1024 * 1024 

resume_router = APIRouter(
    prefix="/resume",
    tags=["resume"]
)


@resume_router.post("/upload")
async def upload_resume(file:UploadFile, db:Session = Depends(get_db), 
                  current_user:User = Depends(get_current_user)):
    
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="Only PDF files are allowed"
        )
        
    
    content = await file.read(MAX_FILE_SIZE + 1)
    
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Resume must not exceed 5MB limit"
        )
        
    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )
        
    try:
        
        resume_service = ResumeService(db)
        resume_storage_service = ResumeStorageService(client)
        logger.info("resume services are initialized")
        
        user_id = current_user.id
        
        storage_path = resume_storage_service.upload(
            user_id,
            content
        )
        logger.info("storage path is received")
        
        new_resume = resume_service.upload_resume(
            user_id,
            storage_path
        )
        
        logger.info("New resume has uploaded")
        
        return {
            "message": "Resume uploaded successfully",
            "resume_id": str(new_resume.id)
        }
        
   
    finally:
        
       await file.close()
    
@resume_router.post("/make_default")
def make_default(resume_id:uuid.UUID , 
                 db:Session = Depends(get_db), 
                 current_user:User = Depends(get_current_user)):
    
    
    user_id = current_user.id
    resume_service = ResumeService(db)
    
    selected_resume = resume_service.select_default(
        user_id,
        resume_id
    )
    
    logger.info(f"{resume_id} set to default")
    
    return {
        
        "message": "Resume set to default successfully",
        "resume_id": resume_id
    }
    
    
    
    
    
    
    