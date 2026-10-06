
import asyncio
import json
import dotenv
import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from sources.topjob_source import TopJobSource

app = FastAPI()

dotenv.load_dotenv()
session_secret = os.getenv("Session_Secret")

app.add_middleware(
    SessionMiddleware,
    secret_key=session_secret
)


async def main():
    
    topjob = TopJobSource()
    response = await topjob.search_job("software","IT-SWare/DB/QA/Web/Graphics/GIS")
    await topjob.get_job_details(response)
    
   
        
    
if __name__ == "__main__":
    
    asyncio.run(main())