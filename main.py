import asyncio
import json
from sources.topjob_source import TopJobSource



async def main():
    
    topjob = TopJobSource()
    response = await topjob.search_job("software","IT-SWare/DB/QA/Web/Graphics/GIS")
    await topjob.get_job_details(response)
    
   
        
    
if __name__ == "__main__":
    
    asyncio.run(main())