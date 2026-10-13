
import uuid

from sqlalchemy.orm import Session

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
        
        
        
    def make_default(self, resume:Resume) -> Resume:
        
        try:
            
            resume.is_default = True
            self.db.commit()
            self.db.refresh(resume)
            
            return resume
            
        except Exception:
            logger.exception('Unexpected error in make default')
            raise