import uuid

from pydantic import BaseModel


class WorkflowResumeRequset(BaseModel):
    
    workflow_id: uuid.UUID
    query: str
    resume_path: str