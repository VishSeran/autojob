import json
import uuid

from sqlalchemy.orm import Session

from configs.logger import get_logger
from repositories.google_connection_repository import GoogleConnectionRepository
from services.encryption_service import EncryptionService

logger = get_logger("google-connection-service")

class GoogleConnectionService:
    
    def __init__(self, db:Session):
        
        self.repo = GoogleConnectionRepository(db)
        self.encryption = EncryptionService()
        
    
    def save_credentials(self, user_id: uuid.UUID, google_email:str, credentials):
        
        try:
            
            if credentials is None:
                raise ValueError("Google authentications credentials are empty")
            
            
            exists_data = self.repo.get_by_user_id(user_id)
            
            encrypted_access_token = self.encryption.encrypt(
                credentials.token
            )
            
            encrypted_refresh_token = (
                self.encryption.encrypt(
                    credentials.refresh_token
                )
                if credentials.refresh_token
                else None
            )
            
            scopes = json.dumps(
                credentials.scopes or []
            )
            
            if exists_data:
                logger.info(f"exisitng data founded: {user_id}")
                
                exists_data.google_email = google_email
                exists_data.access_token_encrpt = encrypted_access_token
                
                
                if encrypted_refresh_token:
                    exists_data.refresh_token_encrpt = (
                        encrypted_refresh_token
                    )
                    
                exists_data.scope = scopes
                
                exists_data.token_expiry = credentials.expiry
                logger.info(f"exisitng data updated: {user_id}")
                
                return self.repo.update(exists_data)
                
                
                
                
        except ValueError:
            logger.exception("Unexpected value error in save credentials")
            raise
        
        except Exception:
            logger.exception("Unexpected error in save credentials")
            raise