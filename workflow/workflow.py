
from langgraph.graph import StateGraph

from configs.logger import get_logger
from workflow.workflow_state import WorkflowState

logger = get_logger("agent-workflow")

class AgentWorkflow:
    
    def __init__(self):
        
        try:
            
            self.graph = None
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
        
        
    async def query_handler_node(state:WorkflowState):
        
        try:
            
            query = state.get("query", "")
            
            if query is None:
                final_answer = "It seems like you have no questions my friend."
                
                return {
                    "final_response" : final_answer
                }
                

        except ValueError:
            logger.exception("Unexpected value error in query handler node")
            raise    
        
        except Exception:
            logger.exception("Unexpected error in query handler node")
            raise