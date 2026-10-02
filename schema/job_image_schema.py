from pydantic import BaseModel


class JobDetails(BaseModel):
    
    job_titile: str | None = None
    company_email: str | None = None
    company_contact: str | None = None
    description: str | None = None
    responsibilities: str | None = None
    requirements: str | None = None
    salary: str | None = None