
from sqlalchemy.orm import Session

from configs.logger import get_logger
from models.gmail import GmailModel


logger = get_logger("gmail-repository")

class GmailRepository:
    
    def __init__(self, db:Session):
        self.db = db
        
        
    def create_gmail(self, gmail:GmailModel):
        
        try:
            
            self.db.add(gmail)
            self.db.commit()
            self.db.refresh(gmail)

            logger.info(f"new gmail added: {gmail.id}")
            
        except Exception:
            logger.exception("Unexpected error in create gmail")
            raise
        
        
        
        