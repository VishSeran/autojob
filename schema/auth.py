
import uuid

from pydantic import BaseModel, Field, EmailStr


class SignUpRequest(BaseModel):
    
    name: str = Field(
        min_length=1,
        max_length=100,
        description="user's preferred name"
    )
    
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128
    )
    
    
class LogInRequest(BaseModel):
    
    email: EmailStr
    password:str
    
    
class UserResponse(BaseModel):
    
    id: uuid.UUID
    name: str | None
    email: EmailStr
    
    model_config = {
        "from_attributes": True
    }
    
    
class LogInResponse(BaseModel):
    
    message: str
    user: UserResponse
    
    