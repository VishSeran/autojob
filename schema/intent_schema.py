

from typing import Literal


class IntentSchema:
    
    intent: Literal[
        "job_search",
        "conversation"
    ]
    
    reasoning: str