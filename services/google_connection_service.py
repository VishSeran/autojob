

from configs.logger import get_logger
from repositories.google_connection_repository import GoogleConnectionRepository


logger = get_logger("google-connection-service")

class GoogleConnectionService:
    
    def __init__(self, google_repository: GoogleConnectionRepository):
        
        self.repo = google_repository
        
    
    def save_credentials(self, credentials):
        
        try:
            
            pass
        except ValueError:
            logger.exception("Unexpected value error in save credentials")
            raise
        
        except Exception:
            logger.exception("Unexpected error in save credentials")
            raise