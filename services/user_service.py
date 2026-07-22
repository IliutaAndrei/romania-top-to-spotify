from datetime import datetime, timedelta, timezone

from fastapi import Depends, Request

from database.database import get_db
from models.user import User
from repositories.user_repository import save_or_update_user, get_user_by_id
from services.spotify_service import exchange_auth_code_for_access_token, get_current_user_profile




def get_current_user(request: Request, db_session=Depends(get_db)) -> User | None:
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    current_user = get_user_by_id(user_id=user_id, session=db_session)

    if not current_user:
        return None

    return current_user


def authenticate_user(code: str, db_session):
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

    db_user = save_or_update_user(user_data, db_session)

    return db_user
