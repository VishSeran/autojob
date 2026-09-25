from configs.logger import get_logger
from mcp_client.client import MCPClient
from schema.topjob_summary_schema import TopJobSummary

logger = get_logger("topjob-client-server-source")
class TopJobClientServerSource:
    
    def __init__(self, mcp_client: MCPClient):
        
        self.mcp_client = mcp_client
        
    async def search_jobs(
        self,
        keyword: str,
        location: str,
        field: str,
        limit: str
    ):
        
        try:
            
            response = await self.mcp_client.call_tool(
                
                "search_jobs",
                {
                    "keyword": keyword,
                    "category": field,
                    "location": location,
                    "limit": limit
                }
            )
            
            return response
            
        except Exception:
            logger.exception("Unexpected error in search jobs")
            raise
        
    async def get_jobs_details(
        self,
        jobs: list[TopJobSummary]
    ):
        
        try:
            
            response = await self.mcp_client.call_tool(
                "get_job_details",
                {
                    "jobs": jobs
                }
            )
            
            return response
            
        
        except Exception:
            logger.exception("Unexpected error in get_jobs_details")
            raise