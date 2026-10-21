
from models.workflow import WorkflowData
from sqlalchemy.orm import Session

class WorkflowRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    
    def create(self, workflow:WorkflowData):
        
        try:
            
            
        