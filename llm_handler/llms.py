import os
import dotenv

from pydantic import SecretStr
from langchain_groq import ChatGroq

from configs.configurations import BASE_CACHE, GROQ_MODEL
from configs.logger import get_logger


logger = get_logger("llm-handler")

dotenv.load_dotenv()

class LLMHandler:
    
    def __init__(self, temperature:float = 0.2):
        
        try:
            
            groq_api = os.getenv("GROQ_API")
            
            if not groq_api:
                raise ValueError("Groq api key is missing")
            
            self.llm = ChatGroq (
                model=GROQ_MODEL,
                cache=True,
                verbose=True,
                api_key=SecretStr(groq_api),
                temperature=temperature,
            )
            
        except Exception:
            logger.exception("Error in llm handler initialization")
            raise
            