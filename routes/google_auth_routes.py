
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from auth.google_auth import create_google_oauth_flow


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
async def google_callback(request:Request):
    
    
    saved_state = request.session.get("google_oauth_state")
    
    if not saved_state:
        raise ValueError ("OAuth state is missing")
    
    flow = create_google_oauth_flow(state=saved_state)
    
    authorization_response = str(request.url)
    
    flow.fetch_token(
        authorization_response = authorization_response
    )
    
    credentials = flow.credentials
    
    
    return {
        "message": "Gmail connected successfully",
        "has_access_token": bool(credentials.token),
        "has_refresh_token": bool(credentials.refresh_token),
        "scopes": credentials.granted_scopes
    }
    
    

    
    


