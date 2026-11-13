import os

import dotenv
from configs.settings import settings
from langchain_openai import ChatOpenAI

from pydantic import SecretStr

from configs.configurations import VISION_MODEL
from configs.logger import get_logger

dotenv.load_dotenv()
logger = get_logger("vision-llm-handler")
class VisionLLmHandler:
    
    def __init__(self, model="gpt-5.4-mini", reasoning_effort: str = "medium"):
        
        
        try:
            
            openai_api = settings.OPENAI_API
                        
            if not openai_api:
                raise ValueError("Groq api key is missing")
            
            self.vision_llm = ChatOpenAI(
                model=model,
                api_key=SecretStr(openai_api),
                reasoning_effort=reasoning_effort
            )
            
            logger.info("vision model has initialized")
        
        except ValueError:
            logger.exception("Value error in vision llm hanlder")
            raise
           
        except Exception:
            logger.exception("Error in vision llm handler initialization")
            raise
        
        
    def get_vision_llm(self,):
        return self.vision_llm