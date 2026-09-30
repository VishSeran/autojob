

from configs.logger import get_logger


logger = get_logger("resume-db")

class ResumeDB:
    
    def __init__(self):
        
        try:
            pass
        except Exception:
            logger.exception("Unexpected error in resume db")
            raise