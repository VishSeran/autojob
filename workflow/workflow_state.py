
from typing import TypedDict

from langchain_core.documents import Document

from schema.job_schema import Job
from schema.resume_schema import ResumeSchema
from schema.topjob_summary_schema import TopJobSummary


class WorkflowState(TypedDict):
    
    query: str
    
    source: str
    keyword: str
    location: str
    job_field: str
    no_of_jobs: int
    
    current_resume: list[Document]
    profile: ResumeSchema
    
    topjob_summary: list[TopJobSummary] 
    topjob_images_urls: dict 
    topjob_images_details: dict 
    topjob_complete_job_details: dict
    
    complete_job_details: list[Job]
 
    job_relevance_score: float
    is_relevance: bool
    
    updated_resume: ResumeSchema
    cover_letter: str
    
    final_response: dict
     