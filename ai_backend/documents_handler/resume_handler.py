from pathlib import Path
from tempfile import NamedTemporaryFile

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader

from configs.configurations import STORAGE_DIR
from configs.logger import get_logger
from services.resume_storage_service import ResumeStorageService

STORAGE_DIR.mkdir(exist_ok=True, parents=True)
logger = get_logger("resume-handler")

class ResumeDocumentHandler:
    
    def __init__(self):
    
        self.current_resume_path = None
        self.storage_service = ResumeStorageService()
        self.loader = None
        self.documents = None
        
        
    def load_from_storage(self, bucket_name:str, file_path:str):
        
        try:
            
            if not bucket_name:
                raise ValueError(
                    "Bucket name is missing"
                )

            if not file_path:
                raise ValueError(
                    "Resume file path is missing"
                )
                
            file_content = self.storage_service.download(file_path)
            logger.info("File bytes downloaded successfully")
            
            extension = (
                Path(
                    file_path
                ).suffix
                .lower()
            )
            
            if extension not in [
                ".pdf",
            ]:
                raise RuntimeError(
                    "Uploaded document is not in supported format"
                )
                
            with NamedTemporaryFile(
                suffix=extension,
                delete=False
            ) as temp_file:
                
                temp_file.write(file_content)
                temp_path = temp_file.name
                
            return self.load(temp_path)
        
        except Exception:
            logger.exception("Unexpected error in load from storage")
            raise
        
    def load(self, resume_path: str | None = None):
        
        try:
         
            if not resume_path:
                raise ValueError("Resume is not found") 
            
            if Path(resume_path).suffix.lower() == ".pdf":
                
                self.loader = PyPDFLoader(resume_path)
                
            elif Path(resume_path).suffix.lower() == ".docx":
                
                self.loader = Docx2txtLoader(resume_path)
                
            else:
                raise RuntimeError("Uploaded document is not in support format")
            
            self.documents = self.loader.load()
            return self.documents
        
        except ValueError:
            logger.exception("Unexpected value error in resume handler")
            raise
      
        except Exception:
            logger.exception("Unexpected error in resume handler")

    
        
        