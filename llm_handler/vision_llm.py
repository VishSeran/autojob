import dotenv
import os
from langchain_groq import ChatGroq

from configs.configurations import VISION_MODEL
from configs.logger import get_logger


dotenv.load_dotenv()
logger = get_logger("vision-llm-handler")
class VisionLLmHandler:
    
    def __init__(self, vision_model = VISION_MODEL):
        
        
        try:
            
            groq_api_key = os.getenv("GROQ_API")
            
            if not groq_api_key:
                raise ValueError("Api key is missing")
            
            self.vision_llm = ChatGroq(
                model=vision_model,
                temperature=0.2,
                cache=True,
                api_key=groq_api_key,
                verbose=True
            )
            
            logger.info("vision model has initialized")
        
        except ValueError:
            logger.exception("Value error in vision llm hanlder")
            raise
           
        except Exception:
            logger.exception("Error in vision llm handler initialization")
            raise
        
        
    def get_vision_llm(self):
        return self.vision_llm