from google_auth_oauthlib.flow import Flow

from configs.settings import settings
from configs.logger import get_logger

logger = get_logger("google-auth")


#only creates an OAuth configuration object containing:
    # your client ID
    # your client secret
    # requested scopes
    # redirect URI
    
def create_google_oauth_flow(state: str | None = None):
    
    try:
        
        flow = Flow.from_client_secrets_file(
            client_secrets_file=settings.CLIENT_SECRET,
            scopes=["https://www.googleapis.com/auth/gmail.send"],
            state = state
        )
        
        flow.redirect_uri(settings.REDIRECT_URI)
        return flow
        
    except Exception:
        logger.exception("Unexpected error in create google oauth flow")
        raise