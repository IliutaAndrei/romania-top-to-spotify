import base64
import pprint
import secrets
from urllib.parse import urlencode

import requests
from sqlalchemy.orm import Session

from config import CLIENT_ID, REDIRECT_URI, AUTHORIZATION_SCOPE, CLIENT_SECRET
from constans import BASE_AUTH_URL, BASE_TOKEN_URL, BASE_API_URL, SEARCH_API_ENDPOINT, PLAYLIST_API_ENDPOINT, \
    BASE_ADD_ITEM_TO_PLAYLIST_ENDPOINT
from models.user import User
from services.token_service import get_valid_access_token

current_state = None


def add_tracks_to_playlist(playlist_id: str, track_ids: list, user: User, db_session: Session):
    access_token = get_valid_access_token(user, db_session)
    endpoint = f"{BASE_ADD_ITEM_TO_PLAYLIST_ENDPOINT}/{playlist_id}/items"

    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}

    uris = [f"spotify:track:{track_id}" for track_id in track_ids]
    payload = {
        "uris": uris
    }

    response = requests.post(endpoint,
                             headers=headers,
                             json=payload)
    response.raise_for_status()
    response_data = response.json()

    return response_data


def create_new_playlist(user: User, db_session: Session, chart_date: str):
    access_token = get_valid_access_token(user, db_session)
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}

    payload = {
        "name": f"Billboard Hot 100 - {chart_date}",
        "description": (
            f"Billboard Hot 100 Top 100 songs for the week of {chart_date}. "
            "Automatically synced to Spotify."
        ),
        "public": True
    }

    response = requests.post(PLAYLIST_API_ENDPOINT,
                             headers=headers,
                             json=payload)
    response.raise_for_status()
    response_data = response.json()

    return response_data


def get_spotify_track_ids(song_list: list[dict[str, str]], user: User, db_session: Session) -> list[str]:
    track_ids = []
    for song in song_list:
        track_id = get_track_spotify_id(song, user, db_session)

        if not track_id:
            continue

        track_ids.append(track_id)

    print(len(track_ids))
    return track_ids


def get_track_spotify_id(track: dict[str, str], user: User, db_session: Session) -> str | None:
    access_token = get_valid_access_token(user, db_session)
    artist = track["artist"]
    title = track["title"]

    headers = {'Authorization': f"Bearer {access_token}"}
    query_params = {"q": f"track:{title} artist:{artist}",
                    "type": "track"}

    response = requests.get(url=SEARCH_API_ENDPOINT,
                            params=query_params,
                            headers=headers)
    response.raise_for_status()
    response_data = response.json()

    if response_data["tracks"]["items"]:
        track_id = response_data["tracks"]["items"][0]["id"]
        print("Song: ")
        pprint.pprint(response_data["tracks"]["items"][0]["artists"][0]["name"])
        pprint.pprint(response_data["tracks"]["items"][0]["name"])
        print()
        return track_id

    return None


def get_current_user_profile(access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    result = requests.get(BASE_API_URL, headers=headers)

    return result.json()


def exchange_auth_code_for_access_token(auth_code: str) -> dict:
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_header = base64.b64encode(credentials.encode("ascii")).decode("ascii")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Basic {auth_header}"
    }

    payload = {
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    response = requests.post(BASE_TOKEN_URL,
                             headers=headers,
                             data=payload)
    response.raise_for_status()
    response_data = response.json()

    return response_data


def get_authorization_url() -> str:
    scope = AUTHORIZATION_SCOPE
    state = secrets.token_urlsafe(16)

    global current_state
    current_state = state

    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'state': current_state
    }

    return BASE_AUTH_URL + urlencode(params)
