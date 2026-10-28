from abc import ABC, abstractmethod

from schema.topjob_category_schema import TopJobCategory

class JobSource(ABC):
    
    @abstractmethod
    async def search_job(
        self,
        keyword: str,
        category: TopJobCategory | None = None,
        location: str | None = None,
        limit: int | None = 10
    ):
        
        pass
    
    @abstractmethod
    async def get_job_details(self, job_url):
        
        pass
    
    