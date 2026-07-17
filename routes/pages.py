from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

from config import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, name="dashboard.html"
    )

@router.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    return templates.TemplateResponse(
        request=request, name="error.html"
    )