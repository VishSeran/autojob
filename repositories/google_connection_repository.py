
from sqlalchemy.orm import Session

from configs.logger import get_logger
from models.google_connection import GoogleConnection

logger = get_logger("google-connection")

class GoogleConnectionRepository:
    
    def __init__(self, db:Session):
        
        self.db = db
        
        
    def create(self, connection: GoogleConnection):
        
        try:
            
            self.db.add(connection)
            self.db.commit()
            self.db.refresh(connection)
            
            return connection
            
        except Exception:
            logger.exception("Unexpected error in create")
            raise
        
        