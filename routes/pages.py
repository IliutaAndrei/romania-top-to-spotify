from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from config import templates
from services.user_service import get_current_user

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user=Depends(get_current_user)):
    if not current_user:
        return RedirectResponse("/")

    return templates.TemplateResponse(
        request=request, name="dashboard.html", headers={"Cache-Control": "no-store"}
    )


@router.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    return templates.TemplateResponse(
        request=request, name="error.html"
    )
