from pydantic import BaseModel, ConfigDict, Field


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


# # from pydantic import BaseModel, ConfigDict


# class StrictSchema(BaseModel):
#     model_config = ConfigDict(extra="forbid")


# # class ExperienceSchema(StrictSchema):
# #     role: str | None
# #     company: str | None
# #     employment_type: str | None
# #     start_date: str | None
# #     end_date: str | None
# #     responsibilities: list[str]
# #     achievements: list[str]
# #     technologies: list[str]


# # class ProjectSchema(StrictSchema):
# #     name: str | None
# #     description: str | None
# #     responsibilities: list[str]
# #     technologies: list[str]
# #     outcomes: list[str]
# #     url: str | None


# # class ResumeSchema(StrictSchema):
# #     personal_details: list[str]
# #     education: list[str]
# #     skills: list[str]
# #     experiences: list[ExperienceSchema]
# #     projects: list[ProjectSchema]
# #     certifications: list[str]
# #     extra_curricular_activities: list[str]



# class ExperienceSchema(BaseModel):
#     role: str | None = None
#     company: str | None = None
#     employment_type: str | None = None
#     start_date: str | None = None
#     end_date: str | None = None
#     responsibilities: list[str] = Field(default_factory=list)
#     achievements: list[str] = Field(default_factory=list)
#     technologies: list[str] = Field(default_factory=list)


# class ProjectSchema(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     responsibilities: list[str] = Field(default_factory=list)
#     technologies: list[str] = Field(default_factory=list)
#     outcomes: list[str] = Field(default_factory=list)
#     url: str | None = None


# class ResumeSchema(StrictSchema):
#     personal_details: dict 
#     education: list[dict]
#     skills: dict
#     experiences: list[dict]
#     projects: list[dict]
#     certifications: list[dict]
#     extra_curricular_activities: list[dict]


#from pydantic import BaseModel, ConfigDict


# class StrictSchema(BaseModel):
#     model_config = ConfigDict(extra="forbid")


# class PersonalDetails(StrictSchema):
#     name: str | None
#     email: str | None
#     phone: list[str] | None
#     location: str | None
#     linkedin: str | None
#     github: str | None
#     portfolio: str | None


# class Education(StrictSchema):
#     degree: str | None
#     field_of_study: str | None
#     institution: str | None
#     location: str | None
#     study_period: str | None
#     gpa: str | None
#     relevant_academic_information: str | None


# class Experience(StrictSchema):
#     job_title: str | None
#     company: str | None
#     employment_type: str | None
#     start_date: str | None
#     end_date: str | None
#     responsibilities: list[str]
#     achievements_and_contributions: list[str]
#     technologies_and_tools_used: list[str]


# class Project(StrictSchema):
#     name: str | None
#     description: str | None
#     responsibilities: list[str] | None
#     technologies: list[str] | None
#     key_features: list[str] | None
#     outcomes: list[str] | None
#     url: str | None


# class Certification(StrictSchema):
#     name: str | None
#     issuing_organization: str | None
#     completion_date: str | None


# class ExtraCurricularActivity(StrictSchema):
#     activity: str | None
#     organization: str | None
#     role: str | None


# class ResumeSchema(StrictSchema):
#     personal_details: PersonalDetails
#     education: list[Education]
#     skills: list[str]
#     experiences: list[Experience]
#     projects: list[Project]
#     certifications: list[Certification]
#     extra_curricular_activities: list[ExtraCurricularActivity]