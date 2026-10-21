
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import select

from configs.logger import get_logger
from models.workflow import WorkflowData

logger = get_logger("workflow-repository")
class WorkflowRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    
    def create(self, workflow:WorkflowData):
        
        try:
            
            self.db.add(workflow)
            self.db.commit()
            self.db.refresh(workflow)
            
            logger.info("New workflow data added successfully")
            return workflow
            
        except Exception:
            logger.exception("Unexpected error in create")
            raise
        
        
    def get_by_user_id(self, user_id:uuid.UUID) -> list[WorkflowData]:
        
        try:
            stmt = (
                select(WorkflowData).where(
                    WorkflowData.user_id == user_id
                )
            )
            
            return list(self.db.scalars(stmt).all())
            
        except Exception:
            logger.exception("Unexpected error in get by user id")
            raise   
        
        
    def get_by_id()