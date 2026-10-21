
from configs.logger import get_logger
from models.workflow import WorkflowData
from sqlalchemy.orm import Session



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