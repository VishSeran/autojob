
import dotenv
import os

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    
    databse_url = 