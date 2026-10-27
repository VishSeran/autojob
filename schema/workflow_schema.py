import uuid
from typing import Literal

from pydantic import BaseModel


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