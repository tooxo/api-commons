from typing import List, Optional

import spotify
import spotify.validation
from common.utils import regex_search


def build_auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def extract_track_list(
    parsed_response: dict,
) -> Optional[List["spotify.Track"]]:
    if "tracks" not in parsed_response:
        return None
    if isinstance(parsed_response["tracks"], list):
        return parsed_response["tracks"]
    return parsed_response["tracks"]["items"]


def extract_id(url: str):
    return regex_search(
        regex=spotify.validation.SPOTIFY_URL_REGEX,
        test_string=url,
        group_no="id",
        should_raise=True,
    )
