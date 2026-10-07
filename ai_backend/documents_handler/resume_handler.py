from pathlib import Path

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader

from configs.configurations import STORAGE_DIR
from configs.logger import get_logger

STORAGE_DIR.mkdir(exist_ok=True, parents=True)
logger = get_logger("resume-handler")

class ResumeDocumentHandler:
    
    def __init__(self):
    
        self.current_resume_path = None
        self.loader = None
        self.documents = None
        
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

    
        
        