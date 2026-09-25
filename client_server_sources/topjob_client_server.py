

from mcp_client.client import MCPClient


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
            
            
        except Exception:
            logger.ex