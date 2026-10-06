

import json
from pathlib import Path


TOKEN_FILE = Path("token_store.json").resolve()


def save_credentials(credentials):
    
    data = {
        
        "token": credentials.token,
        "refersh_token": credentials.refersh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": list(credentials.scopes or [])
        
    }
    
    
    with TOKEN_FILE.open("w") as file:
        
        json.dump(
            data,
            file,
            indent=4
        )
        
        
# Recreate credentials later
# Now imagine tomorrow your LangGraph workflow reaches:
# send_email_node

# There is no browser OAuth login happening anymore.
# You load the saved credentials.

def load_credentials():
    
    pass