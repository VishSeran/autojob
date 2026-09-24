
from configs.logger import get_logger
from llm_handler.llms import LLMHandler


logger = get_logger("query-handler-agent")

class QueryHandlerAgent:
    
    def __init__(self):
        
        
        try:
            self.llm = LLMHandler()
            logger.info("LLM is initialized")
            
            
        except Exception:
            logger.exception("Unexpected error in query handler agent initialization")
            raise