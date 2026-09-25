from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from configs.logger import get_logger

logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self, server_url):
        
        try:
            
            if not server_url:
                raise ValueError("Server URL is missing")

            self.exit_stack = AsyncExitStack()
            self.connected = False
            self.server_url = server_url
            self.session = None
            
        except ValueError:
            logger.exception("Value error in mcp initizlization")
            raise
            
        except Exception:
            logger.exception("Unexpected error in mcp client init")
            raise
        
    async def init_connection(self):
        
        try:
            
            if self.connected:
                raise RuntimeError("Already connected to the server")
            
            if self.session:
                raise RuntimeError("Session is already running")
            
            
            read, write, _ = await self.exit_stack.enter_async_context(
                
                streamable_http_client(self.server_url)
                
            )
            
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(
                    read,
                    write,
                )
            )
            
            await self.session.initialize()
            self.connected = True
            logger.info("MCP session has created")
            
        except Exception:
            logger.exception("Unexpected error in connecting to server")
            self.session = None
            self.connected = False
            self.exit_stack = AsyncExitStack()
            raise
        
        
    async def call_tool(self, tool_name: str, arguments: dict):
        
        try:
            
            if not tool_name:
                raise ValueError("Tool name is missing")
            
            if not arguments:
                raise ValueError("argumrnts are missing")
            
            if self.session is None or not self.connected:
                raise RuntimeError("MCP client is not connected")
            
            
            results = await self.session.call_tool(
                tool_name,
                arguments
            )
            
            logger.info("Tool results is fetched")
            return results
             
        except ValueError:
            logger.exception("Unexpected value error in tool calling")
            raise    
        
        except Exception:
            logger.exception("Unexpected error in tool calling")
            raise
        
    async def close(self):
        
        try:
            
            if self.connected:
                await self.exit_stack.aclose()
            
            self.session = None
            self.connected = False
            self.exit_stack = AsyncExitStack()
            
            logger.info("Connection closed successfully")
            
        except Exception:
            logger.exception("Unexpected error in close connection")
            raise