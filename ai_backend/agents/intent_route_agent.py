

from ai_backend.llm_handler.llms import LLMHandler
from configs.logger import get_logger
from schema.intent_schema import IntentSchema


logger = get_logger("Intent-router-agent")

class IntentRouteAgent:
    
    def __init__(self):
        
        llm_handler = LLMHandler()
        self.llm = llm_handler.get_llm().with_structured_output(IntentSchema)
        
        logger.info("Intent agent has initialized")
        
    
    async def get_intent_response(self, query:str, messages:list) -> IntentSchema:
        
        try:
            history = "\n".join(
                f"{message.type}: {message.content}"
                for message in messages[-10:]
            )
            
            prompt = f"""
                You are the intent router for an AI job-search assistant.

                Determine what the user wants.

                Possible intents:

                1. job_search
                Use this when the user wants to:
                - search for jobs
                - find jobs
                - look for jobs
                - search for a different job
                - find jobs in a location
                - find jobs based on a skill, role, or category

                2. conversation
                Use this for:
                - general questions
                - asking about previous results
                - asking for explanations
                - asking about skills
                - asking about the application process
                - casual conversation

                Conversation history:
                {history}

                Current user message:
                {query}

                Return the correct intent.
                """
                
            response = await self.llm.ainvoke(prompt)
            logger.info("Intent response has fetched")
            logger.info(f"Intent response: \n{response.intent}\n{response.reasoning}")
            
            return response
            
            
        except Exception:
            logger.exception("Unexpected error in intent agent response")
            raise
        
        