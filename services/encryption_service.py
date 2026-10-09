from cryptography.fernet import Fernet

from configs.settings import settings
from configs.logger import get_logger


logger = get_logger("encryption-service")

class EncryptionService:
    
    def __init__(self):
        
        #creates a Fernet encryption/decryption object.
        self.ferent = Fernet(
            key=settings.TOKEN_ENCRYPTION_KEY.encode() #use encode to convert str into bytes
        )
        
    def encrypt(self, value: str | None) -> str | None:
        
        try:
            
            if value:
            
                encrypt_value = self.ferent.encrypt(
                    value.encode()
                ).decode()
                logger.info("Encryption is completed")
            
                return encrypt_value
            
            return None
        
        except Exception:
            logger.exception("Unexpected error in encrypt")
            raise
        
        
        