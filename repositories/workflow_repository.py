
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import select

from configs.logger import get_logger
from models.workflow import WorkflowRun

logger = get_logger("workflow-repository")
class WorkflowRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    
    def create(self, workflowrun:WorkflowRun):
        
        try:
            
            self.db.add(workflowrun)
            self.db.commit()
            self.db.refresh(workflowrun)
            
            logger.info("New workflow run data added successfully")
            return workflowrun
            
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
            
            logger.info("Workflow run data retrieved successfully")
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
            logger.info("Workflow run data retrieved successfully")
            return self.db.scalar(stmt)
            
        except Exception:
            logger.exception("Unexpected error in get by id")
            raise  
        
        
    def delete_by_id(self, workflowrun:WorkflowRun):
        
        try:
            
            self.db.delete(workflowrun)
            self.db.commit()
            
            logger.info("Workflow run data deleted successfully")
            return workflowrun
            
        except Exception:
            logger.exception("Unexpected error in delete")
            raise  
                
             
             