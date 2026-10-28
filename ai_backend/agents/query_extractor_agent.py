from langchain_core.prompts import ChatPromptTemplate

from ai_backend.llm_handler.llms import LLMHandler
from configs.logger import get_logger
from schema.query_schema import QuerySchema

logger = get_logger("query-handler-agent")

class QueryHandlerAgent:
    
    def __init__(self):
        
        try:
            self.llm_handler = LLMHandler()
            self.llm = self.llm_handler.get_llm().with_structured_output(
                QuerySchema,
                method="json_schema",
                strict=True
            )
            
            logger.info("LLM is initialized")
            
            self.prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
                        You are a job search query extraction agent.

                        Analyze the user's job search query and extract:

                        - keyword: Job title, skill, or search keyword.
                        - location: Preferred job location, only if explicitly specified.
                        - category: Map the user's job intent to the most appropriate supported job category when there is a clear match.
                        - number_of_jobs: Number of jobs requested, only if specified.

                        Category rules:
                        - "software", "software engineer", "developer", "web developer",
                        "QA", "database", "frontend", "backend", "full stack"
                        -> IT-SWare/DB/QA/Web/Graphics/GIS

                        - "network engineer", "system engineer", "hardware",
                        "network administrator"
                        -> IT-HWare/Networks/Systems

                        - "telecom", "telecommunications"
                        -> IT-Telecoms

                        - "accounting", "auditing", "finance"
                        -> Accounting/Auditing/Finance

                        - "banking", "insurance"
                        -> Banking & Finance/Insurance

                        - "mechanical engineer", "electrical engineer",
                        "automotive engineer"
                        -> Eng-Mech/Auto/Elec

                        If the user's query does not clearly match any supported category,
                        return null for category.

                        Other rules:
                        - If location is not mentioned, return null.
                        - If number_of_jobs is not mentioned, return null.
                        - Do not invent a location.
                        - Do not invent a category when there is no clear semantic match.
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