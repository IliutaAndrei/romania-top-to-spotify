import base64
import secrets
from urllib.parse import urlencode

import requests

from config import CLIENT_ID, REDIRECT_URI, AUTHORIZATION_SCOPE, CLIENT_SECRET
from constans import BASE_AUTH_URL, BASE_TOKEN_URL, BASE_API_URL

current_state = None


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
