from pydantic import BaseModel


class JobImageDetails(BaseModel):
    
    description: str | None = None
    responsibilities: str | None = None
    requirements: str | None = None