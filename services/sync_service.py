from sqlalchemy.orm import Session

from models.user import User
from services.billboard_service import get_songs, get_chart_date
from services.spotify_service import get_spotify_track_ids, create_new_playlist, add_tracks_to_playlist


def sync_billboard(url: str, user: User, db_session: Session):
    songs = get_songs(url)
    chart_date = get_chart_date(url)

    track_ids = get_spotify_track_ids(songs, user, db_session)

    playlist = create_new_playlist(user, db_session, chart_date)

    add_tracks_to_playlist(playlist["id"],track_ids, user, db_session)

    return playlist