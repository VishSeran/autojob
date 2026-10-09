from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from configs.logger import get_logger
from models.google_connection import GoogleConnection

logger = get_logger("google-connection")

class GoogleConnectionRepository:
    
    def __init__(self, db:Session):
        
        self.db = db
        
        
    def create(self, connection: GoogleConnection) -> GoogleConnection:
        
        try:
            
            self.db.add(connection)
            self.db.commit()
            self.db.refresh(connection)
            
            return connection
            
        except Exception:
            logger.exception("Unexpected error in create")
            raise
        
    
    def get_by_user_id(self, id:UUID) -> GoogleConnection | None:
        
        try:
            
            stmt =  (
                select(GoogleConnection).where(GoogleConnection.user_id == id)
            )
            
            return self.db.scalar(stmt)
            
        except Exception:
            logger.exception("Unexpected error in get by user id")
            raise
            
        
    def update(self, connection:GoogleConnection) -> GoogleConnection:
        
        try:
            
            self.db.add(connection)
            self.db.commit()
            self.db.refresh(connection)
            
            return connection
            
        except Exception:
            self.db.rollback()
            logger.exception("Unexpected error in update")
            raise
        
        
    def delete(self, connection: GoogleConnection) -> GoogleConnection:
        
        try:
            
            
            if connection is None:
                raise ValueError("Connection ORM object is missing")
            
            self.db.delete(connection)
            self.db.commit()
            
            return connection
        
        except ValueError:
            self.db.rollback()
            logger.exception("Unexpected value error in delete")
            raise
            
        except Exception:
            self.db.rollback()
            logger.exception("Unexpected error in delete")
            raise