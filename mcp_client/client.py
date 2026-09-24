from contextlib import AsyncExitStack
from mcp import ClientSession

from configs.logger import get_logger

logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self, server_url, root_dir, ):
        
        try:
            
            if not server_url:
                raise ValueError("Server URL is missing")
            
            if not root_dir:
                raise ValueError("Root dir is mising")
        
            self.exit_stack = AsyncExitStack()
            self.connected = False
            self.server_url = server_url
            self.root_dir = root_dir
            self.session = None
            
        except ValueError:
            logger.exception("Value error in mcp initizlization")
            raise
            
        except Exception:
            logger.exception("Unexpected error in mcp client init")
            raise
        
    async def init_connection(self):
        
        try:
            if self.session:
                raise RuntimeError("Session is already running")
            
            
            
            
        except Exception:
            logger.exception("Unexpected error in connecting to server")
            raise