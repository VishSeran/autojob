
from typing import TypedDict

from schema.job_schema import Job
from schema.topjob_summary_schema import TopJobSummary


class WorkflowState(TypedDict):
    
    query: str
    
    source: str
    keyword: str
    location: str
    job_field: str
    no_of_jobs: int
    current_resume: str
    
    topjob_summary: list[TopJobSummary]
    topjob_images_urls: dict
    topjob_images_details: dict
    topjob_complete_job_details: dict
    
    #job_summary: list[TopJobSummary]
    complete_job_details: list[Job]
 
    job_relavance_score: float
    is_relavance: bool
    
    updated_resume: str
    cover_letter: str
    
    final_response: dict
     