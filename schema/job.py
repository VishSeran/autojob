from pydantic import BaseModel
from typing import Optional


class Job(BaseModel):
    
    source: str
    job_id: str
    job_url: str
    title: str
    company: str
    
    description: Optional[str] = None
    responsibilities: Optional[str] = None
    requirments: Optional[str] = None
    
    location: Optional[str] = None
    salary: Optional[str] = None
    closing_date: Optional[str] = None
    