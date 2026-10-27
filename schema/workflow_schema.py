from typing import Literal
import uuid

from pydantic import BaseModel

job_selection_decision = 

class WorkflowStartRequset(BaseModel):
    
    query: str
    resume_path: str
class WorkflowResumeRequset(BaseModel):
    
    workflow_id: uuid.UUID
    # query: str
    # resume_path: str
    
class JobSelectionInterrupt(BaseModel):
    
    workflow_id: uuid.UUID
    decision: Literal[
    "approve",
    "reject"
    ]