

from pydantic import BaseModel, Field


class GoogleLoginRequest(BaseModel):
    
    name: str = Field(
        min_length=1,
        max_length=100,
        description="User;s preferred display name"
    )