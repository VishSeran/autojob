

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
    
    workflow_service = WorkflowService(db,checkpointer)
    workflow, new_workflow = await workflow_service.create_workflow(
        user_id
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
    
    workflow_service = WorkflowService(db,checkpointer)
    
    initial_state = {
        "query": data.query,
        "current_resume": data.resume_path,
        "current_job_index": 0,
        "rejected_jobs": [],
        "user_decision": None,
        "email_details": None,
        "email_review_response": None,
        "email_sent": False,
        "final_response": None,
    }
    
    
    response = await workflow_service.continue_workflow(
        user_id,
        data.workflow_id,
        initial_state
    )
    
    logger.info("Response has received successfully")
    
    return {
        "workflow_id": str(data.workflow_id),
        "response": response
    }
    
    
    

    


