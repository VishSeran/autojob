from configs.logger import get_logger


CLIENT_SECRET = "secret/client_secret.json"
REDIRECT_URL = "http://localhost:8000/auth/google/callback"


logger = get_logger("google-auth")

def create_google_oauth_flow(state: str | None = None):
    
    try:
        
    except Exception:
        logger.exception("Unexpected error in create google oauth flow")
        raise