from abc import ABC, abstractmethod

class JobSource(ABC):
    
    @abstractmethod
    async def search_job(self, keyword: str, location: str | None,field: str, limit: int = 10):
        
        pass
    
    @abstractmethod
    async def get_job_details(self, job_url):
        
        pass
    
    