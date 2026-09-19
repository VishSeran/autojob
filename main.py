import asyncio

from sources.topjob_source import TopJobSource



async def main():
    
    topjob = TopJobSource()
    response = await topjob.search_job("Network engineer","sri lanka","IT-HWare/Networks/Systems")
    
    with open("job_details", "w") as file:
        file.write(response)
    
if __name__ == "__main__":
    
    asyncio.run(main())