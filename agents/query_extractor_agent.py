from langchain_core.prompts import ChatPromptTemplate

from configs.logger import get_logger
from llm_handler.llms import LLMHandler
from schema.query_schema import QuerySchema

logger = get_logger("query-handler-agent")

class QueryHandlerAgent:
    
    def __init__(self):
        
        try:
            self.llm_handler = LLMHandler()
            self.llm = self.llm_handler.get_llm().with_structured_output(QuerySchema)
            
            logger.info("LLM is initialized")
            
            self.prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
                        You are a job search query extraction agent.

                        Analyze the user's job search query and extract the following:

                        - keyword: Job title, skill, or search keyword.
                        - location: Preferred job location, if specified.
                        - field: Industry or job category, if specified.
                        - number_of_jobs: Number of jobs requested, if specified.

                        If a field is not mentioned in the user's query,
                        return null for that field.

                        Do not invent information that is not present in the query.
                        """
                    ),
                    (
                        "human",
                        "{query}"
                    )
                ]
            ) 
                
            self.query_chain = self.prompt | self.llm
            logger.info("query chain has created")
            
        except Exception:
            logger.exception("Unexpected error in query handler agent initialization")
            raise
        
        
    async def get_response(self, query):
        
        try:
            
            if not query:
                raise ValueError("User query is missing")
            
            response = await self.query_chain.ainvoke({
                "query": query
            })
            
            logger.info("Response has fetched by query handler successfully")
            return response
            
        except ValueError:
            logger.exception("Unexpected value error in query handler get response")
            raise
         
        except Exception:
            logger.exception("Unexpected error in query handler get response")
            raise