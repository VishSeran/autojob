
from logging.handlers import QueueHandler

from langgraph.graph import StateGraph

from agents.query_extractor_agent import QueryHandlerAgent
from configs.logger import get_logger
from schema.query_schema import QuerySchema
from workflow.workflow_state import WorkflowState

logger = get_logger("agent-workflow")

class AgentWorkflow:
    
    def __init__(self):
        
        try:
            
            self.graph = None
            self.query_handler = QueryHandlerAgent()
            self.build_workflow()
            
        except Exception:
            logger.exception("Unexpected error in agent workflow")
            raise
        
        
    def build_workflow(self):
        
        try:
            
            self.graph = StateGraph(WorkflowState)
            
        except Exception:
            logger.exception("Unexpected error in build workflow")
            raise
        
        
    async def query_handler_node(self, state:WorkflowState):
        
        try:
            
            query = state.get("query", "")
            
            if not query:
                final_answer = "It seems like you have no questions my friend."
                
                return {
                    "final_response" : final_answer
                }
                
            response: QuerySchema = await self.query_handler.get_response(query)
            logger.info("query response is fetched")
            
            return {
                "keyword": response.keyword,
                "location": response.location,
                "job_field": response.field,
                "no_of_jobs": response.number_of_jobs
            }
                

        except ValueError:
            logger.exception("Unexpected value error in query handler node")
            raise    
        
        except Exception:
            logger.exception("Unexpected error in query handler node")
            raise