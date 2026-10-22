

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from configs.logger import get_logger
from database.session import get_db
from dependencies.auth import get_current_user
from models.users import User
from schema.workflow_schema import WorkflowResumeRequset
from services.workflow_service import WorkflowService

logger = get_logger("workflow-router")

workflow_router = APIRouter(
    prefix="/workflow",
    tags=["workflow"]
)


@workflow_router.post("/create")
async def create_workflow(
    
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    user_id = current_user.id
    checkpointer = request.app.state.langgraph_checkpointer
    logger.info("checkpointer fetched")
    
    workflow_service = WorkflowService(db)
    workflow_service.
    workflow, new_workflow = workflow_service.create_workflow(
        user_id,
        checkpointer
    )
    logger.info("New workflow created successfully")
    
    return {
        "message": "New workflow created successfully",
        "workflow_id": new_workflow.id
    }
    
@workflow_router.post("/continue")
async def continue_workflow(
    data: WorkflowResumeRequset,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    
    user_id = current_user.id
    checkpointer = request.app.state.langgraph_checkpointer
    logger.info("checkpointer fetched")
    
    workflow_service = WorkflowService(db)
    
    current_workflow = workflow_service.get_workflow_by_id(
        user_id,
        data.workflow_id
    )
    
    

    


