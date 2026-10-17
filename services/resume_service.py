
import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session
from supabase import Client

from configs.logger import get_logger
from database.supabase_client import client
from models.resume import Resume
from repositories.resume_respository import ResumeRepository
from repositories.user_repository import UserRepository
from services.resume_storage_service import ResumeStorageService

logger = get_logger("resume-service")

class ResumeService:
    
    
    def __init__(self, db:Session, client:Client = client):
        
        self.resume_repository = ResumeRepository(db)
        self.user_repository = UserRepository(db)
        self.storage_service = ResumeStorageService(client)
        
        
    def upload_resume(self,content:bytes, user_id:uuid.UUID) -> Resume:
        
        try:
            
            if not user_id:
                raise ValueError("User ID is missing")
            
            user = self.user_repository.get_by_id(user_id)
            
            if user is None:
                raise ValueError("User not found")
            
            storage_path = self.storage_service.upload(
                user_id,
                content
            )
            
            if not storage_path:
                raise ValueError("Storage path is missing")
            
            new_resume = Resume(
                
                user_id = user_id,
                storage_path = storage_path
            )

            self.resume_repository.add_resume(new_resume)
            logger.info(f"Resume {new_resume.id} added for user {user_id}")
            
            return new_resume

        except Exception:
            logger.exception("Unexpected error in upload resume")
            raise
        
        
    def remove_resume(self,user_id:uuid.UUID, resume_id:uuid.UUID) -> Resume:
        
        try:
            
            if resume_id is None:
                raise ValueError("Resume ID is missing")
            
            if user_id is None:
                raise ValueError("User ID is missing")

            wanted_resume = self.resume_repository.get_by_id(
                resume_id,
                user_id
            )
            
            if wanted_resume is None:
                raise ValueError("Resume not found")
            
            if wanted_resume.user_id != user_id:
                raise ValueError("Resume does not belong to user")
            
            storage_path = wanted_resume.storage_path
                            
            if storage_path is None:
                raise HTTPException(
                    status_code=401,
                    detail="Resume storage path is missing"
                )
                
            self.storage_service.delete(
                    storage_path
            )

            deleted_resume = self.resume_repository.delete(wanted_resume) 
            
            return deleted_resume
        
        except Exception:
            logger.exception("Unexpected error in remove resume")
            raise
        
        
    def select_default(self, user_id:uuid.UUID, resume_id:uuid.UUID):
        
        try:
            
            if resume_id is None:
                raise ValueError("Resume ID is missing")
            
            selected_resume = self.resume_repository.get_by_id(
                resume_id,
                user_id
            )
            
            if selected_resume is None:
                raise ValueError("Resume not found")
            
            if selected_resume.user_id != user_id:
                raise ValueError("Resume does not belong to user")
            
            self.resume_repository.make_default(
                selected_resume
            )
            
            logger.info(f"{selected_resume.id} is set to default successfully")
            return selected_resume
        
        except Exception:
            logger.exception("Unexpected error in select default")
            raise
        
        
    def get_all_resumes(self, user_id:uuid.UUID) -> list[Resume]:
        
        try:
            
            if user_id is None:
                raise ValueError("User ID is missing")
            
            user = self.user_repository.get_by_id(user_id)
            
            if user is None:
                raise ValueError("User not found")
            logger.info(f"User has fetched:{user_id}")
            
            resumes = self.resume_repository.get_by_user_id(user_id)
            logger.info(f"User resumes are fetched: {user_id}")
            
            return resumes
        
        except Exception:
            logger.exception("Unexpected error in get all resumes")
            raise
        
        
    def get_resume(self, user_id:uuid.UUID, resume_id: uuid.UUID) -> Resume:
        
        try:
            if user_id is None:
                raise ValueError("User ID is missing")
            
            if resume_id is None:
                raise ValueError("Resume ID is missing")
            
            resume = self.resume_repository.get_by_id(
                resume_id,
                user_id
            )
            
            if resume is None:
                raise ValueError("Resume not found")
                        
            if resume.user_id != user_id:
                raise ValueError("Unauthoried access to resumes")
            
            logger.info(f"{resume_id} resume is retrieved")
            return resume
            
        except Exception:
            logger.exception(f"Unexpected error in {resume_id} resume")
            raise
        
        
    def download_resume(self, user_id:uuid.UUID, resume_id:uuid.UUID) -> bytes:
        
        try:
            
            if user_id is None:
                raise ValueError("User ID is missing")
            
            resume = self.get_resume(
                user_id,
                resume_id
            )
            
            storage_path = resume.storage_path
                
            if storage_path is None:
                raise ValueError(
                    "Resume storage path is missing"
                )

            file_content = self.storage_service.download(storage_path)
            logger.info("file has started downloading")
            
            return file_content
            
        except Exception:
            logger.exception('Unexpected error in resume downloading')
            raise
        
        
    

    