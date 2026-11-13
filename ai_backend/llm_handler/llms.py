import os

import dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from configs.settings import settings
from pydantic import SecretStr

from configs.configurations import GROQ_MODEL
from configs.logger import get_logger

logger = get_logger("llm-handler")

dotenv.load_dotenv()

class LLMHandler:
    
    def __init__(self, model="gpt-5.4-mini", reasoning_effort: str = "medium"):
        
        try:
            
            openai_api = settings.OPENAI_API
            
            if not openai_api:
                raise ValueError("Groq api key is missing")
            
            self.llm = ChatOpenAI(
                model=model,
                api_key=SecretStr(openai_api),
                reasoning_effort=reasoning_effort
            )
            
            logger.info("LLM is initialized success")
            
        except ValueError:
            logger.exception("Value error in llm handler init")
            raise
            
        except Exception:
            logger.exception("Error in llm handler initialization")
            raise
        
        
    def get_llm(self):
        
        return self.llm
    
    async def get_llm_response(self, query):
        
        
        try:
            
            if not query:
                raise ValueError("Query is missing")
            
            response = await self.llm.ainvoke(query)
            logger.info("Response is fetched successfully")
            
            return response
            
        except ValueError:
            logger.exception("Value error in get llm response")
            raise
        
        except Exception:
            logger.exception("Error in get llm response")
            raise
            