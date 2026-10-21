
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import select

from configs.logger import get_logger
from models.workflow import WorkflowRun

logger = get_logger("workflow-repository")
class WorkflowRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    
    def create(self, workflow:WorkflowRun):
        
        try:
            
            self.db.add(workflow)
            self.db.commit()
            self.db.refresh(workflow)
            
            logger.info("New workflow data added successfully")
            return workflow
            
        except Exception:
            logger.exception("Unexpected error in create")
            raise
        
        
    def get_by_user_id(self, user_id:uuid.UUID) -> list[WorkflowRun]:
        
        try:
            stmt = (
                select(WorkflowRun).where(
                    WorkflowRun.user_id == user_id
                )
            )
            
            return list(self.db.scalars(stmt).all())
            
        except Exception:
            logger.exception("Unexpected error in get by user id")
            raise   
        
        
    def get_by_id(self, user_id:uuid.UUID, id:uuid.UUID):
        
        try:
            
            stmt = (
                
                select(WorkflowRun).where(
                    WorkflowRun.id == id,
                    WorkflowRun.user_id == user_id
                )
            )
            
            return self.db.scalar(stmt)
            
        except Exception:
            logger.exception("Unexpected error in get by id")
            raise   