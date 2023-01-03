import json
import typing
from typing import List, Type

import api_commons.spotify as spotify
from api_commons.common.utils import has_aiohttp
from api_commons.common.web import get_request_sync, get_request_async
from .utils import build_auth_header, extract_track_list


class SearchType:
    ALBUM = "album"
    ARTIST = "artist"
    PLAYLIST = "playlist"
    TRACK = "track"
    SHOW = "show"
    EPISODE = "episode"


BASE_URL = "https://api.spotify.com/v1/search?q={}&type={}&limit={}&offset={}"


def _build_search_url(query: str, search_type: List[Type[SearchType]] = (), include_external: bool = True,
                      limit: int = 50, offset: int = 0, market: str = ""):
    formatted = BASE_URL.format(
        query,
        ",".join(
            map(
                lambda x: str(x),
                search_type
            )
        ),
        limit,
        offset
    )
    if include_external:
        formatted += "&include_external=audio"
    if market != "":
        formatted += "&market=" + market

    return formatted


def _parse_search_response(
        search_response: dict
):
    response = []
    if "albums" in search_response:
        response += [
            spotify.Album.from_api_response(json.dumps(x))
            for x in search_response["albums"]["items"]
        ]
    if "artists" in search_response:
        response += [
            spotify.Artist.from_api_response(json.dumps(x))
            for x in search_response["artists"]["items"]
        ]
    if "playlists" in search_response:
        response += [
            spotify.Playlist.from_api_response(json.dumps(x))
            for x in search_response["playlists"]["items"]
        ]
    if "tracks" in search_response:
        response += [
            spotify.Track.from_api_response(json.dumps(x))
            for x in extract_track_list(search_response)
        ]

    return response


def search(
        search_term: str,
        token: str,
        search_result_count: int = 5,
        search_result_offset: int = 0,
        search_type: List[Type[SearchType]] = None,
        include_external: bool = True
) -> List[
    typing.Union[
        "spotify.Album", "spotify.Artist", "spotify.Playlist", "spotify.Track",
    ]
]:
    if search_type is None:
        search_type = [SearchType.TRACK]
    if search_type in [SearchType.SHOW, SearchType.EPISODE]:
        raise NotImplemented
    response: dict = json.loads(
        get_request_sync(
            url=_build_search_url(query=search_term, search_type=search_type, include_external=include_external,
                                  limit=search_result_count, offset=search_result_offset),
            extra_headers=build_auth_header(token),
        )
    )
    return _parse_search_response(response)


@has_aiohttp
async def search_async(
        search_term: str,
        token: str,
        search_result_count: int,
        search_result_offset: int = 0,
        search_type: List[Type[SearchType]] = None,
        include_external: bool = True
) -> List[typing.Union[spotify.Album, spotify.Track, spotify.Artist, spotify.Playlist]]:
    if search_type is None:
        search_type = [SearchType.TRACK]

    if SearchType.SHOW in search_type or SearchType.EPISODE in search_type:
        raise NotImplemented
    response: dict = json.loads(
        await get_request_async(
            url=_build_search_url(query=search_term, search_type=search_type, include_external=include_external,
                                  limit=search_result_count, offset=search_result_offset),
            extra_headers=build_auth_header(token),
        )
    )
    return _parse_search_response(response)
