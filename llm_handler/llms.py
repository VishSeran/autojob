from langchain_groq import ChatGroq

from configs.configurations import BASE_CACHE, GROQ_MODEL
from configs.logger import get_logger


logger = get_logger("llm-handler")

class LLMHandler:
    
    def __init__(self, temperature:float = 0.2):
        
        try:
            
            self.llm = ChatGroq (
                name=GROQ_MODEL,
                cache=BASE_CACHE,
                verbose=True,
                temperature=temperature
            )
            
        except Exception:
            logger.exception("Error in llm handler initialization")
            raise
            