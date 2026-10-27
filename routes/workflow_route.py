

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from configs.logger import get_logger
from database.session import get_db
from dependencies.auth import get_current_user
from models.users import User
from schema.workflow_schema import (
    JobSelectionInterrupt,
    WorkflowResumeRequset,
    WorkflowStartRequset,
)
from services.workflow_service import WorkflowService

logger = get_logger("workflow-router")

workflow_router = APIRouter(
    prefix="/workflow",
    tags=["workflow"]
)


@workflow_router.post("/create")
async def create_workflow(
    data: WorkflowStartRequset,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    user_id = current_user.id
    checkpointer = request.app.state.langgraph_checkpointer
    logger.info("checkpointer fetched")
    
    workflow_service = WorkflowService(db,checkpointer)
    
    initial_state = {
        
        "user_id": user_id,
        "query": data.query,
        "current_resume_id": data.resume_path,
        "current_job_index": 0,
        "rejected_jobs": [],
        "user_decision": None,
        "email_details": None,
        "email_review_response": None,
        "email_sent": False,
        "final_response": None,
    }
        
    response, new_workflow = await workflow_service.create_workflow(
        user_id,
        initial_state
    )
    
    logger.info("New workflow created successfully")
    
    return {
        "message": "New workflow created successfully",
        "workflow_id": new_workflow.id,
        "response": response
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
    workflow = workflow_service.get_workflow_by_id(user_id, data.workflow_id)
    
    # initial_state = {
        
    #     "user": current_user,
    #     "query": data.query,
    #     "current_resume_id": data.resume_path,
    #     "current_job_index": 0,
    #     "rejected_jobs": [],
    #     "user_decision": None,
    #     "email_details": None,
    #     "email_review_response": None,
    #     "email_sent": False,
    #     "final_response": None,
    # }
    
    
    response = await workflow_service.continue_workflow(
        user_id,
        data.workflow_id,
    )
    
    logger.info("Response has received successfully")
    
    interrupts = response.get("__interrupt__", [])
    
    if interrupts:
        logger.info("Interrupt detected")
        interrupt_data = interrupts[0]
        
        return {
            "status": "interrupt",
            "thread_id": workflow.thread_id,
            "interrupt": interrupt_data
        }
        
        
    return {
        
        "workflow_id": str(data.workflow_id),
        "response": response
    }
    
@workflow_router.post("/continue/resume")   
async def interrupt_resume(
    data: JobSelectionInterrupt,
    request:Request,
    current_user: User = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    
    user_id = current_user.id
    checkpointer = request.app.state.langgraph_checkpointer
    
    workflow_service = WorkflowService(
        db,
        checkpointer
    )
    
    resume_data = {
        "decision": data.decision
    }
    
    logger.info(f"User decision is fetched: {resume_data}")
    
    response = await workflow_service.resume_workflow(
        user_id,
        data.workflow_id,
        resume_data
    )
    
    return {
        
        "workflow_id": str(data.workflow_id),
        "response": response
    }
    
@workflow_router.post("/continue/finalize")
async def final_response_interrupt(
    request: Request,
    data:
)
    
    
    
    
    

    


