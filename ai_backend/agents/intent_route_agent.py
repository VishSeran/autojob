

from ai_backend.llm_handler.llms import LLMHandler
from configs.logger import get_logger


logger = get_logger("Intent-router-agent")

class IntentRouteAgent:
    
    def __init__(self):
        
        self.llm = LLMHandler().get_llm()
        
        self.system_prompt = 