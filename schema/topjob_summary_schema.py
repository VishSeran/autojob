from pydantic import BaseModel


class TopJobSummary(BaseModel):
    
    job_title: str
    company_name: str
    image_number: int
    
    starting_date: str | None
    closing_date: str | None
    location: str | None
    rid: int 
    ac: str
    jc: str
    ec: str
    token: str