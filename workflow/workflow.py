


from langgraph.graph import StateGraph

from agents.query_extractor_agent import QueryHandlerAgent
from client_server_sources.topjob_client_server import TopJobClientServerSource
from configs.configurations import TOPJOB_SERVER_URL
from configs.logger import get_logger
from mcp_client.client import MCPClient
from schema.query_schema import QuerySchema
from workflow.workflow_state import WorkflowState

logger = get_logger("agent-workflow")

class AgentWorkflow:
    
    def __init__(self):
        
        try:
            
            self.workflow = None
            self.topjob_mcp_client = MCPClient(TOPJOB_SERVER_URL)
            self.topjob_client_server_Source = None
            self.query_handler = QueryHandlerAgent()
            
            logger.info("Agents are initialized")
            self.build_workflow()
            logger.info("Workflow build is completed")
            
        except Exception:
            logger.exception("Unexpected error in agent workflow")
            raise
        
        
    async def initialize(self):
        
        try:
            await self.topjob_mcp_client.init_connection()
            logger.info("Topjob mcp client is connected")
            
            self.topjob_client_server_Source = TopJobClientServerSource(
                self.topjob_mcp_client
            )
            
            
        except Exception:
            logger.exception('Unexpected error in worlflow initialize')
            raise
        
        
        
    def build_workflow(self):
        
        try:
            
            if self.workflow is not None:
                raise RuntimeError("Workflow is already running") 
            
            graph = StateGraph(WorkflowState)
            graph.add_node("query_handler_node", self.query_handler_node)
            
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
        
        
    async def job_search_node(self):
        pass
        