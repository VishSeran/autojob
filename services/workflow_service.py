
import uuid

from sqlalchemy.orm import Session

from ai_backend.workflow.workflow import AgentWorkflow
from configs.logger import get_logger
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
        
        
    def get_workflow_by_thread_id(self, user_id:uuid.UUID, thread_id:uuid.UUID):
        
        try:
            
            if not user_id:
                raise ValueError("User ID is missing")
            
            if not thread_id:
                raise ValueError("Thread ID is missing")
            
            current_workflow = self.workflow_repository.get_by_thread_id(
                user_id,
                thread_id
            )
            
            if current_workflow is None:
                raise ValueError("Workflow not found")
            
            logger.info(f"Current Wokrflow is received successfully: {current_workflow.id}")
            return current_workflow
            
        except Exception:
            logger.exception("Unexpected error in get workflow by id")
            raise
        
        
    def get_workflow_by_id(self, user_id:uuid.UUID, id:uuid.UUID):
            
            try:
                
                if not user_id:
                    raise ValueError("User ID is missing")
                
                if not id:
                    raise ValueError("Thread ID is missing")
                
                current_workflow = self.workflow_repository.get_by_id(
                    user_id,
                    id
                )
                
                if current_workflow is None:
                    raise ValueError("Workflow not found")
                
                logger.info(f"Current Wokrflow is received successfully: {current_workflow.id}")
                return current_workflow
                
            except Exception:
                logger.exception("Unexpected error in get workflow by id")
                raise
            
            
    def get_workflows(self, user_id:uuid.UUID):
        
        try:
            
            if not user_id:
                raise ValueError("User ID is missing")
            
            workflows = self.workflow_repository.get_by_user_id(
                user_id
            )
            
            logger.info("Workflows fetched successfully")
            return workflows
            
        
        except Exception:
            logger.exception("Unexpected error in get workflows")
            raise
        
        
    def delete_workflow(self, id:uuid.UUID, user_id:uuid.UUID):
        
        try:
            
            if not user_id:
                raise ValueError("User ID is missing")

            if not id:
                raise ValueError("Workflow ID is missing")
            
            workflow = self.workflow_repository.get_by_id(
                user_id,
                id
            )
            deleted_workflow = self.workflow_repository.delete_by_id(workflow)
            
            self.db.commit()
            logger.info(f"{deleted_workflow.id} deleted successfully")
            return deleted_workflow
            
        except Exception:
            logger.exception("Unexpected error in delete workflow by id")
            raise
        
    