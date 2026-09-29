

from pydantic import BaseModel


class ResumeSchema (BaseModel):
    
    personal_details: list[str] | None = None
    
    education: list[str] | None = None
    
    skills: list[str] | None = None
    
    experiences: list[dict] | None = None
    
    projects: list[dict] | None = None
    
    certifications: list[str] | None = None
    
    extra_curricular_activities: list[str] | None = None
    
    