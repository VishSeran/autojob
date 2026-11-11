

from ai_backend.llm_handler.llms import LLMHandler
from configs.logger import get_logger
from schema.intent_schema import IntentSchema


logger = get_logger("Intent-router-agent")

class IntentRouteAgent:
    
    def __init__(self):
        
        llm_handler = LLMHandler()
        self.llm = llm_handler.get_llm().with_structured_output(IntentSchema)
        
        logger.info("Intent agent has initialized")
        
    
    async def get_intent_response(self, query, messages):
        
        try:
            
            
        except Exception:
            logger.exception("Unexpected error in intent agent response")
            raise
        
        