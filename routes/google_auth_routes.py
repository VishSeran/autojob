
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from auth.google_auth import create_google_oauth_flow


router = APIRouter(
    prefix="/auth/google",
    tags=["google-auth"]
)

@router.get("")
async def google_login(request:Request):
    
    flow = create_google_oauth_flow()
    
    authorization_url, state = flow.authorization_url(
        access_type = "offline",
        include_granted_scope = True,
        prompt = "consent"
    )
    
    request.session['google_oauth_state'] = state
    return RedirectResponse(authorization_url)