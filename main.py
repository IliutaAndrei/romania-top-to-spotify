from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.pages import router as pages_router
from routes.auth import router as login_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages_router)
app.include_router(login_router)



