import requests
from datetime import datetime, timedelta, timezone

from constans import BASE_API_URL
from database.database import SessionLocal
from repositories.user_repository import save_or_update_user
from services.spotify_service import exchange_auth_code_for_access_token


def get_current_user_profile(access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    result = requests.get(BASE_API_URL, headers=headers)

    return result.json()


def authenticate_user(code: str):
    token_data = exchange_auth_code_for_access_token(code)
    access_token = token_data["access_token"]

    if not access_token:
        raise Exception("Invalid access token")

    profile_data = get_current_user_profile(access_token)

    user_data = {
        "spotify_id": profile_data["id"],
        "display_name": profile_data["display_name"],
        "email": profile_data["email"],
        "access_token": access_token,
        "refresh_token": token_data["refresh_token"],
        "expires_at": datetime.now(timezone.utc) + timedelta(seconds=token_data["expires_in"])
    }

    session = SessionLocal()
    try:
        save_or_update_user(user_data, session)
    finally:
        session.close()

    return user_data
