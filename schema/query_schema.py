from pydantic import BaseModel, Field

from schema.topjob_category_schema import TopJobCategory


class QuerySchema(BaseModel):

    keyword: str = Field(
        description="Job title, skill, or keyword to search for."
    )

    location: str | None = Field(
        default=None,
        description="Preferred job location, such as a city, district, or country."
    )

    field: TopJobCategory | None = Field(
        default=None,
        description="Industry or job category, such as IT, Finance, or Engineering."
    )

    number_of_jobs: int | None = Field(
        default=None,
        description="Maximum number of job listings to retrieve."
    )