import math
import time
from collections.abc import Mapping
from typing import Any

import requests
from dacite import from_dict

from source.constants import (
    BASE_URL,
    CONFIG,
    SLEEP_BETWEEN_REQUESTS,
    TIMEOUT,
    X_API_KEY,
)
from source.types import Artists, Setlists
from source.utils import deep_snake_case_keys


def send_request(params: Mapping[str, int | str], url: str) -> Any:
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en",
        "x-api-key": X_API_KEY,
    }
    response = requests.get(
        f"{BASE_URL}/{url}", headers=headers, params=params, timeout=TIMEOUT
    )
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    return response.json()


def get_mbid(artist_name: str) -> str:
    url = "search/artists"
    params = {"artistName": artist_name, "sort": "relevance"}
    response = send_request(params, url)
    snake_response = deep_snake_case_keys(response)
    artists = from_dict(Artists, snake_response, config=CONFIG)

    if not (artist := artists.artist):
        raise ValueError(f"No artist found with name {artist_name!r}")
    return artist[0].mbid


def get_setlists(mbid: str, artist_name: str) -> Setlists:
    url = "search/setlists"
    params: dict[str, int | str] = {
        "artistMbid": mbid,
        "artistName": artist_name,
    }
    response = send_request(params, url)
    snake_response = deep_snake_case_keys(response)
    setlists_data = from_dict(Setlists, snake_response, config=CONFIG)
    setlist = setlists_data.setlist
    total = setlists_data.total
    items_per_page = setlists_data.items_per_page
    total_pages = math.ceil(total / items_per_page)

    for page in range(2, total_pages + 1):
        params["p"] = page
        response = send_request(params, url)
        snake_response = deep_snake_case_keys(response)
        setlist_data = from_dict(Setlists, snake_response, config=CONFIG)
        setlist.extend(setlist_data.setlist)

    return Setlists(setlist, total, page, items_per_page, setlists_data.type)
