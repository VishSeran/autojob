
from pathlib import Path

from configs.configurations import STORAGE_DIR
from configs.logger import get_logger

STORAGE_DIR.mkdir(exist_ok=True, parents=True)
logger = get_logger("resume-handler")

class ResumeDocumentHandler:
    
    def __init__(self):
        
        self.resume = None
        self.current_resume_path = None
        
    def load(self, resume_path: str | None = None):
        
        try:
            
            if not resume_path:
                self.current_resume_path = self.get_latest_resume()
                logger.info(f"Proceeding with latest uploaded resume: {self.current_resume_path}")
                
            if resume_path:
                self.save_latest_resume(resume_path)
                logger.info(f"resume has saved: {resume_path}")
                self.current_resume_path = resume_path
            
            if not self.current_resume_path:
                raise RuntimeError("Resume is not found") 
            
            if self.current_resume_path.            
                
        
                
        except Exception:
            logger.exception("Unexpected error in resume handler")
            raise
    
    
    def save_latest_resume(self, resume_path):
        
        pass
        
    def get_latest_resume(self):
        
        pass