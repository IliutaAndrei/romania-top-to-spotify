from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from models.user import User

def get_user_by_id(user_id, session: DbSession):
    return session.get(User, user_id)


def save_or_update_user(user_data: dict, session: DbSession):
    stmt = select(User).where(User.spotify_id == user_data["spotify_id"])

    user = session.scalar(stmt)

    if user:
        user.display_name = user_data["display_name"]
        user.email = user_data["email"]
        user.access_token = user_data["access_token"]
        user.refresh_token = user_data["refresh_token"]
        user.expires_at = user_data["expires_at"]
    else:
        user = User(
            spotify_id=user_data["spotify_id"],
            display_name=user_data["display_name"],
            email=user_data["email"],
            access_token=user_data["access_token"],
            refresh_token=user_data["refresh_token"],
            expires_at=user_data["expires_at"]
        )
        session.add(user)

    session.commit()
    session.refresh(user)

    return user
