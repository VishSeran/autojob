
from pydantic import BaseModel


class Job(BaseModel):
    
    source: str
    job_url: list[str]
    title: str
    company_name: str
    company_email: str
    company_contact: str
    
    description: str | None = None
    responsibilities: str | None = None
    requirments: str | None = None
    
    location: str | None = None
    salary: str | None = None
    starting_date : str | None = None
    closing_date: str | None = None
    