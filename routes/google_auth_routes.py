
from fastapi import APIRouter, Request


router = APIRouter(
    prefix="/auth/google",
    tags=["google-auth"]
)

@router.get("")
async def google_login(request:Request)