
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
        
        try:
            
            if user_id is None:
                raise ValueError("User ID is missing")
            
            storage_path = f"{user_id}/{uuid.uuid4()}.pdf"
            
            self.client.storage.from_(
                self.BUCKET_NAME
            ).upload(
                storage_path,
                file_content,
                file_options= {
                    
                    "content-type": "application/pdf"
                }
            )
            
            logger.info("Reumes has uploaded to storage bucket")
            return storage_path
        
        except Exception:
            logger.exception("Unexpected error in upload")
            raise
        
        
    def download(self, storage_path:str):
        
        try:
            
            if not storage_path:
                raise ValueError("storage path is missing")
            
            file_content = self.client.storage.from_(
                self.BUCKET_NAME
            ).download(
                storage_path
            )
            
            logger.info(
                f"File download from storage: {storage_path}"
            )
            
            return file_content
    
        except Exception:
            logger.exception("Unexpected error in download")
            raise
        
        
    def delete(self, storage_path:str):
        
        try:
            
            if not storage_path:
                raise ValueError("storage path is missing")
            
            self.client.storage.from_(
                self.BUCKET_NAME
            ).remove(
                
                [storage_path]
            )
            
            logger.info(
                    f"File deleted from storage: {storage_path}"
            )
            
            return storage_path
            

        except Exception:
            logger.exception("Unexpected error in delete")
            raise