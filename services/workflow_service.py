
import uuid

from sqlalchemy.orm import Session

from ai_backend.workflow.workflow import AgentWorkflow
from configs.logger import get_logger
from models.users import User
from models.workflow import WorkflowRun
from repositories.user_repository import UserRepository
from repositories.workflow_repository import WorkflowRunRepository

logger = get_logger("workflow-service")


class WorkflowService:
    
    def __init__(self, db:Session):
        
        self.db = db
        self.workflow_repository = WorkflowRunRepository(db)
        self.user_repository = UserRepository(db)
        
        logger.info("Repositories are initialized")
        
        
    def create_workflow(self, user_id:uuid.UUID, checkpointer):
        
        try:
            
            if not user_id:
                raise ValueError("User ID is missing")

            if not checkpointer:
                raise ValueError("Checkpointer is missing")
            
            workflow_run = WorkflowRun(
                user_id = user_id,
            )
            
            new_workflow = self.workflow_repository.create(workflow_run)
            
            logger.info("Workflow is added to database successfully")
            
            workflow = AgentWorkflow(
                
                self.db,
                user_id,
                new_workflow.thread_id,
                checkpointer
            )
            
            self.db.commit()
            
            logger.info("Workflow is initialized")
            return workflow
            
        except Exception:
            logger.exception("Unexpected error in create workflow")
            raise
        
        
    def get_workflow_by_id(self, user_id:uuid.UUID, thread_id:uuid.UUID, checkpointer):
        
        try:
            
            if not user_id:
                raise ValueError("User ID is missing")
            
            if not thread_id:
                raise ValueError("Thread ID is missing")

            if not checkpointer:
                raise ValueError("Checkpointer is missing")
            
            current_workflow = self.workflow_repository.get_by_thread_id(
                user_id,
                thread_id
            )
            
        except Exception:
            logger.exception("Unexpected error in get workflow by id")
            raise
