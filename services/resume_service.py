
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
            
            if not user_id or storage_path:
                raise ValueError("User ID or storage path is missing")
            
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
            logger.info("New resume added successfully")
            
            return new_resume

        except Exception:
            logger.exception("Unexpected error in upload resume")
            raise
    
    