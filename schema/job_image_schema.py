from pydantic import BaseModel


class JobDetails(BaseModel):
    
    description: str | None = None
    responsibilities: str | None = None
    requirements: str | None = None