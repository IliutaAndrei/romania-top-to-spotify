import pprint

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from database.database import get_db
from services import spotify_service
from services.spotify_service import get_authorization_url, exchange_auth_code_for_access_token
from services.user_service import authenticate_user

router = APIRouter()

@router.get("/auth/login")
async def login():
    auth_url = get_authorization_url()

    return RedirectResponse(auth_url)


@router.get("/callback")
async def callback(code, state, request: Request, db_session=Depends(get_db)):
    if state != spotify_service.current_state:
        return RedirectResponse("/error")

    db_user = authenticate_user(code, db_session)
    request.session["user_id"] = db_user.id

    return RedirectResponse("/dashboard")

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()

    return RedirectResponse("/")