from pydantic import BaseModel

class JobSummary(BaseModel):
    
    job_title: str
    company_name: str
    image_number: int
    
    starting_date: str
    closing_date: str
    location: str