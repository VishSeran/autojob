
from typing import TypedDict

from schema.topjob_summary_schema import TopJobSummary


class WorkflowState(TypedDict):
    
    query: str
    
    keyword: str
    location: str
    job_field: str
    
    topjob_summary: list[TopJobSummary]
    topjob_images_urls: dict
    topjob_images_details: dict
    topjob_complete_job_details: dict
    
    current_resume: str
    job_relavance_score: float
    is_relavance: bool
    
    updated_resume: str
    cover_letter: str
    
    final_response: dict
     