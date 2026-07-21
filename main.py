from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from config import SECRET_KEY
from routes.pages import router as pages_router
from routes.auth import router as login_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    https_only=False
)
app.include_router(pages_router)
app.include_router(login_router)



