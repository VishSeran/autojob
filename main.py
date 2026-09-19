import asyncio

from sources.topjob_source import TopJobSource



async def main():
    
    topjob = TopJobSource()
    await topjob.search_job("software engineer","sri lanka","IT-SWare/DB/QA/Web/Graphics/GIS",)
    
if __name__ == "__main__":
    
    asyncio.run(main())