from pydantic import BaseModel, Field


class ExperienceSchema(BaseModel):
    role: str | None = None
    company: str | None = None
    employment_type: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)


class ProjectSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    outcomes: list[str] = Field(default_factory=list)
    url: str | None = None


class ResumeSchema(BaseModel):
    personal_details: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    experiences: list[ExperienceSchema] = Field(default_factory=list)
    projects: list[ProjectSchema] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    extra_curricular_activities: list[str] = Field(default_factory=list)