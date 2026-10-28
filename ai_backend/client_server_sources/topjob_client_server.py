import json

from ai_backend.mcp_client.client import MCPClient
from configs.logger import get_logger
from schema.topjob_category_schema import TopJobCategory
from schema.topjob_summary_schema import TopJobSummary

logger = get_logger("topjob-client-server-source")
class TopJobClientServerSource:
    
    def __init__(self, mcp_client: MCPClient):
        
        self.mcp_client = mcp_client
        


    @staticmethod
    def _extract_response(response):

        if response.is_error:
            raise RuntimeError(
                f"MCP tool returned an error: {response.content}"
            )

        if response.structured_content is not None:
            return response.structured_content

        if response.content:

            for item in response.content:

                if hasattr(item, "text"):

                    try:
                        return json.loads(item.text)

                    except json.JSONDecodeError:
                        return item.text

        raise RuntimeError(
            "MCP tool returned no usable content"
        )
        
        
    async def search_jobs(
        self,
        keyword: str,
        location: str,
        category: TopJobCategory | None,
        limit: str
    ):
        
        try:
            
            response = await self.mcp_client.call_tool(
                
                "search_jobs",
                {
                    "keyword": keyword,
                    "category": (
                        
                        category.model_dump()
                        if category is not None
                        else None),
                    
                    "location": location,
                    "limit": limit
                }
            )
            
            raw_jobs = self._extract_response(response)
            logger.info(f"search jobs raw results: {raw_jobs}")
            
            jobs = [
                TopJobSummary.model_validate(job)
                for job in raw_jobs
            ]
            
            
            logger.info(f"search jobs result id fetched: {jobs}")
            return jobs
            
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
                    "jobs": [
                        job.model_dump()
                        for job in jobs
                    ]
                }
            )
            
            logger.info(f"get jobs details results fetched:{response}")
            return self._extract_response(response)
            
        
        except Exception:
            logger.exception("Unexpected error in get_jobs_details")
            raise