
import uuid

from sqlalchemy.orm import Session

from configs.logger import get_logger
from models.resume import Resume


logger = get_logger("resume-repository")

class ResumeRepository:
    
    def __init__(self, db:Session):
        
        self.db = db
        
    
    def add_reume(
        self,
        user_id: uuid.UUID,
        storage_path: str
    ) -> Resume :
        
        try:
            
            
        except Exception