
from fastapi import APIRouter


resume_router = APIRouter(
    prefix="/resume",
    tags=["resume"]
)


@resume_router.post("/upload_resume")