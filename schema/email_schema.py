from pydantic import BaseModel, Field


class EmailSchema(BaseModel):

    subject: str = Field(
        description="Professional email subject for the job application"
    )

    cover_letter: str = Field(
        description="Tailored professional cover letter to include in the job application email"
    )