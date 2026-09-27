from pydantic import BaseModel


class JobDetails(BaseModel):
    
    job_titile: str | None = None
    description: str | None = None
    responsibilities: str | None = None
    requirements: str | None = None