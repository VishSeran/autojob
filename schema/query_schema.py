from typing import Optional
from pydantic import BaseModel, Field

class QuerySchema(BaseModel):

    keyword: str = Field(
        description="Job title, skill, or keyword to search for."
    )

    location: Optional[str] = Field(
        description="Preferred job location, such as a city, district, or country."
    )

    field: Optional[str] = Field(
        description="Industry or job category, such as IT, Finance, or Engineering."
    )

    number_of_jobs: Optional[int] = Field(
        description="Maximum number of job listings to retrieve."
    )