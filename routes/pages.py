import pprint

from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from config import templates
from database.database import get_db
from services.spotify_service import get_current_user_profile
from services.user_service import get_current_user, get_valid_access_token

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
    else:
        access_token = get_valid_access_token(current_user, db_session)
        user_profile = get_current_user_profile(access_token)

        pprint.pprint(user_profile)

    return templates.TemplateResponse(
        request=request, name="dashboard.html"
    )


@router.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    return templates.TemplateResponse(
        request=request, name="error.html"
    )
