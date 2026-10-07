
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from auth.google_auth import create_google_oauth_flow
from auth.token_store import save_credentials

router = APIRouter(
    prefix="/auth/google",
    tags=["google-auth"]
)


@router.get("")
async def google_login(request:Request):
    
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

    flow = create_google_oauth_flow()
    
    authorization_url, state = flow.authorization_url(
        access_type = "offline",
        include_granted_scope = True,
        prompt = "consent"
    )
    
    request.session['google_oauth_state'] = state
    return RedirectResponse(authorization_url)


@router.get("/callback")
async def google_callback(request: Request):

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

    # --------------------------------------------------
    # 7. Save the credentials somewhere secure.
    #
    #    During development you may save them in a local
    #    token file.
    #
    #    In production, save them securely in a database
    #    and associate them with the correct user.
    # --------------------------------------------------
    save_credentials(credentials)

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
    
    

    
    


