from bs4 import BeautifulSoup, Tag
import requests

from constans import TITLE_CSS_SELECTOR, ARTIST_CSS_SELECTOR, SONG_LIST_CSS_SELECTOR, CHART_DATE_CSS_SELECTOR


def _extract_song_details(element: Tag) -> dict[str, str] | None:
    title_element = element.select_one(TITLE_CSS_SELECTOR)
    artist_element = element.select_one(ARTIST_CSS_SELECTOR)

    if not title_element or not artist_element:
        return None

    title = title_element.get_text(strip=True)
    artist = artist_element.get_text(strip=True)

    return {
        "title": title,
        "artist": artist
    }

def _get_html_from_url(link: str) -> str:
    page = requests.get(link)
    page.raise_for_status()

    return page.text


def get_songs(url: str) -> list[dict[str, str]]:
    songs = []

    html = _get_html_from_url(url)
    soup = BeautifulSoup(html, 'html.parser')

    song_list = soup.select(SONG_LIST_CSS_SELECTOR)

    for song in song_list:
        song_details = _extract_song_details(song)
        if song_details is not None:
            songs.append(song_details)

    return songs


def get_chart_date(url: str) -> str:
    html = _get_html_from_url(url)
    soup = BeautifulSoup(html, 'html.parser')

    chart_date_element = soup.select_one(CHART_DATE_CSS_SELECTOR)

    if not chart_date_element:
        raise Exception("Element for date not found!")

    chart_date = chart_date_element.get_text(strip=True)

    return chart_date





