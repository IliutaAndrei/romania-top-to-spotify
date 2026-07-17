from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from services import spotify_service
from services.spotify_service import get_authorization_url, exchange_code_for_access_token, \
    get_current_user_profile


router = APIRouter()

@router.get("/auth/login")
async def login():
    auth_url = get_authorization_url()

    return RedirectResponse(auth_url)


@router.get("/callback")
async def callback(code, state):
    if state == spotify_service.current_state:
        access_token = exchange_code_for_access_token(code)["access_token"]
        # profile_data = get_current_user_profile(access_token)

        return RedirectResponse("/dashboard")
    else:
        return RedirectResponse("/error")
