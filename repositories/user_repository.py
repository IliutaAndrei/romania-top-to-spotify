from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User


def save_or_update_user(user_data: dict, session: Session):
    stmt = select(User).where(User.spotify_id == user_data["spotify_id"])

    existing_user = session.scalar(stmt)

    if existing_user:
        existing_user.display_name = user_data["display_name"]
        existing_user.email = user_data["email"]
        existing_user.access_token = user_data["access_token"]
        existing_user.refresh_token = user_data["refresh_token"]
        existing_user.expires_at = user_data["expires_at"]
    else:
        db_user = User(
            spotify_id=user_data["spotify_id"],
            display_name=user_data["display_name"],
            email=user_data["email"],
            access_token=user_data["access_token"],
            refresh_token=user_data["refresh_token"],
            expires_at=user_data["expires_at"]
        )
        session.add(db_user)

    session.commit()
