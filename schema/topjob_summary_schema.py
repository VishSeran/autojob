from pydantic import BaseModel, Field


class TopJobSummary(BaseModel):
    
    job_title: str
    company_name: str
    image_number: int
    
    starting_date: str | None = None
    closing_date: str | None = None
    location: str | None = None
    rid: int 
    ac: str
    jc: str
    ec: str
    token: str