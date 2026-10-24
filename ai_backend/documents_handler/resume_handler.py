import json
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from sqlalchemy.orm import Session

from configs.configurations import STORAGE_DIR
from configs.logger import get_logger
from services.resume_service import ResumeService

STORAGE_DIR.mkdir(exist_ok=True, parents=True)
logger = get_logger("resume-handler")

class ResumeDocumentHandler:
    
    def __init__(self, db:Session):
    
        self.current_resume_path = None
        self.storage_service = ResumeService(db)
        self.loader = None
        self.documents = None
        logger.info("Resume handler is created")
        
        
    def load_from_storage(self, user_id:uuid.UUID, resume_id:uuid.UUID):
        
        temp_path = None
        
        try:
            

            if not resume_id:
                raise ValueError(
                    "Resume file ID is missing"
                )
                
            file_content = self.storage_service.download_resume(
                user_id,
                resume_id
            )
            
            # logger.info("File bytes downloaded successfully")
            
            # if not isinstance(file_content, bytes):
            #     raise TypeError(
            #         f"Expected PDF bytes, got {type(file_content)}"
            #     )
            
            # if extension != ".pdf":
            #     raise RuntimeError(
            #         "Only PDF resumes are currently supported"
            #     )
            
            if not isinstance(file_content, bytes):
                raise TypeError(
                    f"Expected PDF bytes, got {type(file_content).__name__}"
                )

            if not file_content.startswith(b"%PDF-"):
                raise ValueError("Downloaded content is not a valid PDF file")
            
            logger.info(
                "PDF downloaded successfully. Size: %s bytes",
                len(file_content)
            )
            
            with NamedTemporaryFile(suffix=".pdf", delete=False, ) as temp_file:
                temp_file.write(file_content)
                temp_path = temp_file.name
                
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
            
            logger.info(
            "PDF loaded successfully. Pages: %s",
            len(documents)
            )

            return documents
                
        except Exception:
            logger.exception("Unexpected error in load from storage")
            raise
        
        finally:

            if temp_path:

                path = Path(temp_path)

                if path.exists():

                    try:
                        path.unlink()

                        logger.info(
                            "Temporary resume file deleted"
                        )

                    except Exception:
                        logger.warning(
                            "Failed to delete temporary resume file: %s",
                            temp_path
                        )

        
    def load_docs(self, resume_path: str | None = None):
        
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

    
        
        