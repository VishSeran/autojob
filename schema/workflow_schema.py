import uuid

from pydantic import BaseModel



class WorkflowStartRequset(BaseModel):
    
    query: str
    resume_path: str
class WorkflowResumeRequset(BaseModel):
    
    workflow_id: uuid.UUID
    # query: str
    # resume_path: str