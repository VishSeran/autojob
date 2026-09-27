

from configs.logger import get_logger
from llm_handler.llms import LLMHandler


logger = get_logger("job-relavance-agent")

class JobRelavanceAgent:
    
    def __init__(self):
        
        try:
            
            self.llm_handler = LLMHandler()
            
            self.llm = self.llm_handler.get_llm().with_structured_output()
        except Exception:
            logger.exception("Unexpected error in job relavance agent")
            raise