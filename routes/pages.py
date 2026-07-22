import pprint

from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from config import templates
from constans import BILLBOARD_TOP100_URL
from database.database import get_db
from services.billboard_service import get_songs
from services.spotify_service import get_current_user_profile, get_spotify_track_ids
from services.sync_service import sync_billboard
from services.user_service import get_current_user
from services.token_service import get_valid_access_token

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user=Depends(get_current_user), db_session=Depends(get_db)):
    if not current_user:
        return RedirectResponse("/")

    access_token = get_valid_access_token(current_user, db_session)
    spotify_profile = get_current_user_profile(access_token)

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"user": spotify_profile}
    )


@router.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    return templates.TemplateResponse(
        request=request, name="error.html"
    )


@router.get("/sync")
async def sync(current_user=Depends(get_current_user), db_session=Depends(get_db)):
    if not current_user:
        return RedirectResponse("/")

    playlist = sync_billboard(BILLBOARD_TOP100_URL, current_user, db_session)

    return RedirectResponse("/dashboard")
