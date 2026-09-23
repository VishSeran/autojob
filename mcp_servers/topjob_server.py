from fastmcp import FastMCP
from configs.logger import get_logger


logger = get_logger("mcp-server")

class TopJobMcpServer:
    
    def __init__(self):
        
        try:
            
            self.topjob_server = FastMCP(
                name="AutoJobMcpServer",
                instructions= """
                    This MCP server provides job-search and vacancy-retrieval tools for TopJobs.lk
                    for the Autonomous Job Application Agent.

                    Responsibilities:
                    - Search and filter job vacancies from TopJobs.lk.
                    - Retrieve detailed vacancy information.
                    - Extract and normalize TopJobs-specific job data.
                    - Retrieve job-advertisement images when available.
                    - Return factual information obtained from TopJobs.lk without inventing
                    missing details.
                    - Preserve source-specific identifiers required for further retrieval.
                    - Keep all TopJobs.lk scraping and parsing logic isolated from the
                    downstream agent workflow.

                    The server only handles job discovery and source-specific data retrieval.
                    Image analysis, vision processing, candidate-job matching, relevance
                    evaluation, CV tailoring, cover-letter generation, and application decisions
                    are handled by downstream LangGraph components.

                    The server should return structured, factual job information and clearly
                    represent unavailable or missing information.
                    """
            )
            
            self.register_tools()
            
        except Exception:
            logger.exception("Error in mcp server initialize")
            raise
        
        
    def register_tools(self):
        
        try:
            
            
            
        except Exception:
            logger.exception('Error in regiter tools')
            raise
    
    