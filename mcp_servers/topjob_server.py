from fastmcp import FastMCP
from fastmcp import Context
from configs.logger import get_logger
from schema.topjob_category_schema import TopJobCategory
from schema.topjob_summary_schema import TopJobSummary
from sources.topjob_source import TopJobSource


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
            self.topjob_source = TopJobSource()
            self.register_tools()
            
            logger.info("Top Job Mcp Server uped with tools")
            
        except Exception:
            logger.exception("Error in mcp server initialize")
            raise
        
        
    def register_tools(self):
        
        try:
            
            @self.topjob_server.tool()
            async def search_jobs(ctx:Context,
                                  keyword:str, 
                                  category:TopJobCategory, 
                                  location = None, 
                                  limit:int | None = 10,):
                
                """
                Search and retrieve job vacancies from TopJobs.lk based on
                keyword, functional category, and optional location.

                Returns structured job information including job title, company,
                location, dates, and source identifiers for further retrieval.
                """
                
                try:
                
                    response = await self.topjob_source.search_job(
                        keyword,
                        category,
                        location,
                        limit
                    )
                    
                    await ctx.info(f"{keyword} jobs searched results are fetched")
                    logger.info(f"{keyword} jobs searched results are fetched")
                    return response
                
                except Exception as e:
                    await ctx.error(f"Unexpected error in search job in topjob mcp server: {e}")
                    logger.error(f"Unexpected error in search job in topjob mcp server: {e}")
                    raise
            
            
            @self.topjob_server.tool()
            async def get_job_details(ctx:Context, jobs:list[TopJobSummary]):
                """Retrieve vacancy-detail images for the provided TopJobs.lk jobs.

                Returns:
                    A dictionary where each key is the job title and the corresponding
                    value is a list of image URLs containing the detailed job vacancy
                    information.
                """
                try:
                    
                    response = await self.topjob_source.get_job_detail_images(jobs)
                    await ctx.info("Job images URLs are fetched successfully")
                    logger.info("Job images URLs are fetched successfully")
                    
                    
                    return response
                    
                    
                except Exception as e:
                    await ctx.error(f"Unexpected error in get job details in topjob mcp server: {e}")
                    logger.error(f"Unexpected error in get job details in topjob mcp server: {e}")
                    raise
            
        except Exception:
            logger.exception('Error in regiter tools')
            raise
    
    