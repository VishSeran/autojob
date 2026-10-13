
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import select

from configs.logger import get_logger
from models.resume import Resume


logger = get_logger("resume-repository")

class ResumeRepository:
    
    def __init__(self, db:Session):
        
        self.db = db
        
    
    def add_resume(
        self,
        resume:Resume
    ) -> Resume :
        
        try:
           
           self.db.add(resume) 
           self.db.commit()
           self.db.refresh(resume)
           logger.info(f"{resume.id} is added to bucket")
           
           return resume
     
        except Exception:
            logger.exception('Unexpected error in add resume')
            raise
        
        
    def get_by_id(self, res_id:uuid.UUID) -> Resume | None:
        
        try:
            
            stmt = (
                select(Resume).where(
                    Resume.id == res_id
                )
            )
            
            return self.db.scalar(
                stmt
            )
            
        except Exception:
            logger.exception('Unexpected error in get by id')
            raise
        
    
    def get_by_user_id(self, user_id:uuid.UUID) -> Resume | None:
        
        try:
            
            stmt = (
                select(Resume).where(
                    Resume.user_id == user_id
                )
            )
            
            return self.db.scalar(
                stmt
            )
            
        except Exception:
            logger.exception('Unexpected error in get by user id')
            raise   
        
    def make_default(self, resume:Resume) -> Resume:
        
        try:
            
            resume.is_default = True
            self.db.commit()
            self.db.refresh(resume)
            logger.info(f"{resume.id} is set to default")
            
            return resume
            
        except Exception:
            logger.exception('Unexpected error in make default')
            raise
        
        
    def delete(self, resume:Resume) ->Resume :
        
        try:
            
            self.db.delete(resume)
            self.db.commit()
            self.db.refresh(resume)
            logger.info(f"{resume.id} is deleted successfully")
            
            return resume
            
        except Exception:
            logger.exception('Unexpected error in delete resume')
            raise