from google_auth_oauthlib.flow import Flow

from configs.logger import get_logger


CLIENT_SECRET = "secret/client_secret.json"
REDIRECT_URI = "http://localhost:8000/auth/google/callback"


logger = get_logger("google-auth")


#only creates an OAuth configuration object containing:
    # your client ID
    # your client secret
    # requested scopes
    # redirect URI
    
def create_google_oauth_flow(state: str | None = None):
    
    try:
        
        flow = Flow.from_client_secrets_file(
            client_secrets_file=CLIENT_SECRET,
            scopes=["https://www.googleapis.com/auth/gmail.send"],
            state = state
        )
        
        flow.redirect_uri(REDIRECT_URI)
        return flow
        
    except Exception:
        logger.exception("Unexpected error in create google oauth flow")
        raise