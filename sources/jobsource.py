
from abc import ABC, abstractmethod


class JobScource(ABC):
    
    @abstractmethod
    async def search_job(self, keyword: str, location: str | None, limit: int = 10):
        
        pass
    
    async def get_job_details(self, job_url):
        
        pass
    
    