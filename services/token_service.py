import base64

from datetime import datetime, timezone, timedelta

import requests
from sqlalchemy.orm import Session

from config import CLIENT_ID, CLIENT_SECRET
from constans import BASE_TOKEN_URL
from models.user import User


def get_valid_access_token(user: User, db_session: Session):
    if is_access_token_expired(user):
        token_data = refresh_access_token(user.refresh_token)
        new_access_token = token_data["access_token"]
        user.access_token = new_access_token
        user.expires_at = datetime.now(timezone.utc) + timedelta(seconds=token_data["expires_in"])

        db_session.commit()

    return user.access_token


def is_access_token_expired(user: User) -> bool:
    return user.expires_at <= datetime.now(timezone.utc)


def refresh_access_token(refresh_token: str):
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_header = base64.b64encode(credentials.encode("ascii")).decode("ascii")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Basic {auth_header}"
    }

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(BASE_TOKEN_URL,
                             headers=headers,
                             data=payload)
    response.raise_for_status()
    response_data = response.json()

    return response_data
