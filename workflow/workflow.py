
from langgraph.graph import StateGraph

from configs.logger import get_logger
from workflow.workflow_state import WorkflowState


logger = get_logger("agent-workflow")

class AgentWorkflow:
    
    def __init__(self):
        
        try:
            
            self.build_workflow()
            
        except Exception:
            logger.exception("Unexpected error in agent workflow")
            raise
        
        
    def build_workflow(self):
        
        try:
            
            graph = StateGraph(WorkflowState)
            
        except Exception:
            logger.exception("Unexpected error in build workflow")
            raise
        
        
    async def query_handler_node(state:WorkflowState):
        
        try:
            
            
            
        except Exception
            logger.exception("Unexpected error in query handler node")
            raise