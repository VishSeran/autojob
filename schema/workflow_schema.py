from pydantic import BaseModel


class WorkflowStartRequset(BaseModel):
    
    query: str
    resume: 