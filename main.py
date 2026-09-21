import asyncio
import json
from sources.topjob_source import TopJobSource



async def main():
    
    topjob = TopJobSource()
    response = await topjob.search_job("full stack","All_Vacancies")
    
    
    for job in response:
        with open("job_details", "w") as file:
            file.write(json.dumps(job.model_dump()))
    
if __name__ == "__main__":
    
    asyncio.run(main())