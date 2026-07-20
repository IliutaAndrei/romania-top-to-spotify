import pprint

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from services import spotify_service
from services.spotify_service import get_authorization_url, exchange_auth_code_for_access_token
from services.user_service import authenticate_user

router = APIRouter()

@router.get("/auth/login")
async def login():
    auth_url = get_authorization_url()

    return RedirectResponse(auth_url)


@router.get("/callback")
async def callback(code, state):
    if state != spotify_service.current_state:
        return RedirectResponse("/error")

    profile_data = authenticate_user(code)
    pprint.pprint(profile_data)

    return RedirectResponse("/dashboard")
