import requests
from fastapi import APIRouter, HTTPException, Request

from auth.google_auth import create_google_oauth_flow
from configs.logger import get_logger
from database.session import get_db
from schema.google_login_request import GoogleLoginRequest
from services.google_connection_service import GoogleConnectionService
from services.user_service import UserService
from sqlalchemy.orm import Session
from fastapi import Depends
from services.auth_service import AuthService



logger = get_logger("google-auth-route")

google_auth_router = APIRouter(
    prefix="/auth/google",
    tags=["google-auth"]
)


@google_auth_router.post("")
async def google_login(request:Request, user_data:GoogleLoginRequest):
    
    # What happens in the browser?
    # The user visits:
    # http://localhost:8000/auth/google

    # Your backend responds:
    # 302 Redirect

    # Browser goes to Google:
    # accounts.google.com

    # Google says something like:
    # AutoJobMe wants permission to:

    # Send email on your behalf

    # User clicks:
    # Allow

    # Google then redirects back to:
    # http://localhost:8000/auth/google/callback

    # Something like:
    # http://localhost:8000/auth/google/callback
    #     ?state=abc123
    #     &code=4/0Aea...

    # Two important values come back:
    # state
    # code

    # The code is not your access token.
    # It is a short-lived authorization code.
    name = user_data.name.strip()
    password = user_data.password
    
    
    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )
        
    flow = create_google_oauth_flow()
    logger.info("Flow has created")
    
    authorization_url, state = flow.authorization_url(
        access_type = "offline",
        include_granted_scope = True,
        prompt = "consent"
    )
    logger.info("Authorization url and state are created")
    
    request.session['google_oauth_state'] = state
    request.session['google_registration_name'] = name
    request.session['prefer_password'] = password
    
    return {
        "authorization_url": authorization_url
    }


@google_auth_router.get("/callback")
async def google_callback(request: Request, 
                          db:Session = Depends(get_db)
                          ):

    # --------------------------------------------------
    # 1. Get the OAuth state value that we previously
    #    saved in the user's session before redirecting
    #    them to Google.
    #
    #    This helps us make sure that the callback
    #    belongs to the same OAuth flow we started.
    # --------------------------------------------------
    saved_state = request.session.get(
        "google_oauth_state"
    )
    logger.info("Saved state is fetched")
    
    registration_name = request.session.get(
        "google_registration_name"
    ) 
    prefer_password = request.session.get(
        "prefer_password"
    )

    # --------------------------------------------------
    # 2. If the state is missing, we cannot safely
    #    continue the OAuth flow.
    # --------------------------------------------------
    if not saved_state:
        raise ValueError("OAuth state is missing")

    # --------------------------------------------------
    # 3. Re-create the same Google OAuth Flow object.
    #
    #    We pass the previously saved state value so the
    #    OAuth library knows which authorization flow
    #    this callback belongs to.
    # --------------------------------------------------
    flow = create_google_oauth_flow(
        state=saved_state
    )
    logger.info("flow is created using saved state")

    # --------------------------------------------------
    # 4. Get the full callback URL returned by Google.
    #
    #    It will look something like:
    #
    #    http://localhost:8000/auth/google/callback
    #    ?state=abc123
    #    &code=4/0Aea....
    #
    #    The important part is the temporary
    #    authorization code returned by Google.
    # --------------------------------------------------
    authorization_response = str(request.url)
    logger.info("authorization response is fetched")
    # --------------------------------------------------
    # 5. Exchange the temporary authorization code
    #    for real OAuth credentials.
    #
    #    After this step, Google returns credentials
    #    that may contain:
    #
    #    - access token
    #    - refresh token
    #    - token expiry
    #    - granted scopes
    #
    #    The authorization code itself cannot be used
    #    directly to call the Gmail API.
    # --------------------------------------------------
    flow.fetch_token(
        authorization_response=authorization_response
    )

    # --------------------------------------------------
    # 6. Get the Credentials object from the OAuth flow.
    #
    #    credentials.token
    #        -> current access token
    #
    #    credentials.refresh_token
    #        -> used later to get a new access token
    #           without asking the user to log in again
    # --------------------------------------------------
    credentials = flow.credentials
    logger.info("Credentials are fetched")
    # --------------------------------------------------
    # 7. Save the credentials somewhere secure.
    #
    #    During development you may save them in a local
    #    token file.
    #
    #    In production, save them securely in a database
    #    and associate them with the correct user.
    # --------------------------------------------------
    response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers= {
            "Authorization": f"Bearer {credentials.token}"
        }
    )
    response.raise_for_status()
    
    user_data = response.json()
    
    google_id = user_data["sub"]
    google_email = user_data["email"]
    email_verified = user_data["email_verified"]
    
    if not google_id or not google_email or not email_verified:
        
        raise HTTPException(
            status_code=400,
            detail="Google account information is incomplete or unverified"
        )
    
    
    exisitng_user = user_service.get_user_by_email(google_email)
    
    if exisitng_user:
        ##login
        return None
    
    
    if not registration_name:
        raise HTTPException(
            status_code=400,
            detail="Registration name is missing"
        )
        
    if not prefer_password:
        raise HTTPException(
            status_code=400,
            detail="Password is missing"
        )
        
    
    auth_service = AuthService(db)
    new_user = auth_service.signup(
        email=google_email,
        name = registration_name,
        password=prefer_password
    )
    
    logger.info(f"New user has created: {new_user.id}")
    
    google_connection_service = GoogleConnectionService(db)
    
    new_connection = google_connection_service.save_credentials(
        user_id=new_user.id,
        google_email=google_email,
        credentials=credentials,
        google_id=google_id
    )
    
    logger.info(f"New google connection has established {new_connection.id}")
    
    
    # --------------------------------------------------
    # 8. Remove the OAuth state from the session.
    #
    #    We no longer need it because the OAuth flow has
    #    successfully completed.
    #
    #    pop(..., None) removes the value safely.
    #    If it does not exist, Python returns None
    #    instead of raising an error.
    # --------------------------------------------------
    request.session.pop(
        "google_oauth_state",
        None
    )
    
    request.session.pop(
        "google_registration_name",
        None
    )

    # --------------------------------------------------
    # 9. Return a success response.
    #
    #    At this point, Gmail is connected and your
    #    application can later use the stored refresh
    #    token to call the Gmail API.
    # --------------------------------------------------
    return {
        "message": "Gmail connected successfully"
    }
    
    

    
    


