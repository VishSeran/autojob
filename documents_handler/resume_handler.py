
from configs.configurations import STORAGE_DIR
from configs.logger import get_logger

STORAGE_DIR.mkdir(exist_ok=True, parents=True)
logger = get_logger("resume-handler")

class ResumeHandler:
    
    def __init__(self):
        
        self.resume = None
        
    def load(self, resume_path):
        
        try:
            
            pass
        except Exception:
            logger.exception("Unexpected error in resume handler")
            raise