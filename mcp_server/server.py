from fastmcp import FastMCP
from configs.logger import get_logger


logger = get_logger("mcp-server")

class MCPServer:
    
    def __init__(self):
        
        try:
            
            self.mcp_server = FastMCP(
                name="AutoJobMcpServer",
                instructions= """This MCP server provides job-search and vacancy-retrieval tools
                for the Autonomous Job Application Agent.

                Responsibilities:
                - Search job vacancies from supported job platforms.
                - Retrieve detailed information for a selected vacancy.
                - Normalize job data into a common structured format.
                - Support filtering by job field, keyword, location, and other criteria.
                - Provide job information to downstream LangGraph agents for analysis.
                - Keep job-source-specific logic isolated from the agent workflow.

                Initially, the server supports TopJobs.lk.

                Future supported sources may include:
                - LinkedIn
                - Indeed
                - Company career pages

                The server should return factual job information retrieved from
                supported sources and must not invent missing vacancy details.

                The server is responsible only for job discovery and retrieval.
                Candidate-job matching, CV tailoring, cover-letter generation,
                and application decisions are handled by the LangGraph workflow.
                """
            )
            
            self.register_tools()
            
        except Exception:
            logger.exception("Error in mcp server initialize")
            raise
        
        
    def register_tools(self):
        
        try:
            
            pass
            
        except Exception:
            logger.exception('Error in regiter tools')
            raise
    
    