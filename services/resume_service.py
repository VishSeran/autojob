
import uuid

from sqlalchemy.orm import Session

from configs.logger import get_logger
from repositories.resume_respository import ResumeRepository
from repositories.user_repository import UserRepository
from models.resume import Resume


logger = get_logger("resume-service")

class ResumeService:
    
    
    def __init__(self, db:Session):
        
        self.resume_repository = ResumeRepository(db)
        self.user_repository = UserRepository(db)
        
        
    def upload_resume(self, user_id:uuid.UUID, storage_path: str) -> Resume:
        
        try:
            
            if not user_id:
                raise ValueError("User ID is missing")

            if not storage_path:
                raise ValueError("Storage path is missing")
            
            user = self.user_repository.get_by_id(user_id)
            
            if user is None:
                raise ValueError("User not found")
            
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
        
        
    def remove_resume(self, resume_id) -> Resume:
        
        try:
            
            if resume_id is None:
                raise ValueError("Resume ID is missing")
            
            wanted_resume = self.resume_repository.get_by_id(
                resume_id
            )
            
            if wanted_resume is None:
                raise ValueError("Resume not found")
            
            self.resume_repository.delete(wanted_resume)
            return wanted_resume
        
        except Exception:
            logger.exception("Unexpected error in remove resume")
            raise
        
        
    def select_default(self, resume_id):
        
        try:
            
            if resume_id is None:
                raise ValueError("Resume ID is missing")
            
            selected_resume = self.resume_repository.get_by_id(
                resume_id
            )
            
            if selected_resume is None:
                raise ValueError("Resume not found")
            
            self.resume_repository.make_default(
                selected_resume
            )
            
            logger.info(f"{selected_resume.id} is set to default successfully")
            return selected_resume
        
        except Exception:
            logger.exception("Unexpected error in select default")
            raise

    