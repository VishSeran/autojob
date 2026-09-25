

from configs.logger import get_logger
from mcp_client.client import MCPClient

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
            
            response = await self.mcp_client.
            
        except Exception:
            logger.exception("Unexpected error in searc jobs")
            raise