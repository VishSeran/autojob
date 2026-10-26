
from typing import Literal, TypedDict

from langchain_core.documents import Document

from models.users import User
from schema.job_schema import Job
from schema.resume_schema import ResumeSchema
from schema.topjob_summary_schema import TopJobSummary


class WorkflowState(TypedDict):
    
    query: str
    user: User
    
    source: str = "topjob"
    keyword: str
    location: str | None
    job_field: str | None
    no_of_jobs: int 
    
    current_resume_id: str
    current_resume: list[Document]
    profile_data: ResumeSchema
    
    topjob_summary: list[TopJobSummary] 
    topjob_images_urls: dict 
    topjob_images_details: dict 
    topjob_complete_job_details: dict
    
    complete_job_details: list[Job]
 
    relevant_jobs_list: list[dict]
    current_job_index: int 
    current_job: dict | None
    
    user_decision: dict
    
    approved_jobs: list[Job]
    rejected_jobs: list[Job]
    
    updated_resume: ResumeSchema
    email_details: dict 
    
    email_review_response: dict
    
    email_sent: bool 
    final_response: dict
     