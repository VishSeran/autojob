
import uuid

from supabase import Client

from configs.logger import get_logger


logger = get_logger("resume-storage-service")

class ResumeStorageService:
    
    BUCKET_NAME = "resumes"
    
    def __init__(self,client:Client):
        
        self.client = client
        logger.info("Supabase client has connected")
        
    def upload(self, user_id:uuid.UUID, file_content:bytes):
        
        storage_path = f"{user_id}/{uuid.uuid4}.pdf"
        
        self.client.storage.from_(
            self.BUCKET_NAME
        ).upload(
            storage_path,
            file_content,
            file_options= {
                "content-type":"application/pdf"
            }
        )
        
        logger.info()