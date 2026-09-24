
from pydantic import BaseModel


class Job(BaseModel):
    
    source: str
    job_id: str
    job_url: str
    title: str
    company: str
    
    description: str | None = None
    responsibilities: str | None = None
    requirments: str | None = None
    
    location: str | None = None
    salary: str | None = None
    closing_date: str | None = None
    