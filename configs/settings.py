
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL:str = Field(validation_alias="DATABASE_URL")
    groq_api: str
    session_secret: str
    TOKEN_ENCRYPTION_KEY:str
    CLIENT_SECRET:str
    REDIRECT_URI:str
    JWT_SECRET_KEY:str
    JWT_ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINS:int
    REFRESH_TOKEN_EXPIRE_DAYS:int
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
        
        
settings = Settings()
