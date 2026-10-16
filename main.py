
import asyncio
import os

import dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from routes.auth_route import auth_router
from routes.google_auth_routes import google_auth_router
from routes.user_route import user_router
from routes.resume_route import resume_router
from sources.topjob_source import TopJobSource

app = FastAPI(
    title="AutoJob API"
)

dotenv.load_dotenv()
session_secret = os.getenv("Session_Secret")


#need session to temporary remember OAuth state
app.add_middleware(
    SessionMiddleware,
    secret_key=session_secret
)

app.include_router(
    auth_router
)
app.include_router(
    user_router
)

app.include_router(
    google_auth_router
)

app.include_router(
    resume_router
)


async def main():
    
    topjob = TopJobSource()
    response = await topjob.search_job("software","IT-SWare/DB/QA/Web/Graphics/GIS")
    await topjob.get_job_details(response)
    
   
        
    
if __name__ == "__main__":
    
    asyncio.run(main())