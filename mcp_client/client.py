from contextlib import AsyncExitStack

from mcp.client import ClientSession

from configs.logger import get_logger

logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self, server_url, root_dir, ):
        
        try:
        
            self.exit_stack = AsyncExitStack()
            self.connected = False
            self.server_url = server_url
            self.root_dir = root_dir
            self.session:ClientSession = None
            
        except Exception:
            logger.exception("Unexpected error in mcp client init")
            raise