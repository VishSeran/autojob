
from sqlalchemy.orm import Session

from configs.logger import get_logger

logger = get_logger("google-connection")

class GoogleConnectionRepository:
    
    def __init__(self, db:Session):
        
        self.db = db
        
        