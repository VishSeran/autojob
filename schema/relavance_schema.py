

from typing import Literal

from pydantic import BaseModel, Field


class RelevanceSchema(BaseModel):
    
    relavance_assesment: Literal[
        "Highly relevant",
        "Relevant",
        "Partially relevant",
        "Low relevance"
    ]
    
    relevance_score: int = Field(
        ge=0,
        le=100,
        description="Overall relevance score from 0 to 100"
    ) 
    
    matching_skills: list[str]
    
    missing_requirements: list[str]
    
    relevant_experience: list[str]
    
    explanation: str
    
    concerns: list[str]
    
    