import os

from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

templates = Jinja2Templates(directory="templates")


load_dotenv()

def get_env_value(name):
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing env variable: {name}")

    return value


CLIENT_ID = get_env_value("CLIENT_ID")
CLIENT_SECRET = get_env_value("CLIENT_SECRET")
REDIRECT_URI = get_env_value("REDIRECT_URI")
DATABASE_URL = get_env_value("DATABASE_URL")
SECRET_KEY = get_env_value("SECRET_KEY")


AUTHORIZATION_SCOPE = ('playlist-read-private playlist-modify-private'
                       ' playlist-modify-public user-read-email user-read-private user-library-read')
