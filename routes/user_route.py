from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user
from models.users import User

user_router = APIRouter(
    prefix="/user",
    tags=['user']
)


@user_router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    
    return {
        
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }