import json
from typing import List, Type
import urllib.parse

import typing

import spotify
from common.web import get_request_sync, get_request_async
from spotify.utils import build_auth_header


class SearchType:
    ALBUM = "album"
    ARTIST = "artist"
    PLAYLIST = "playlist"
    TRACK = "track"
    SHOW = "show"
    EPISODE = "episode"


BASE_URL = "https://api.spotify.com/v1/search?q={}&type={}&limit={}"


def _parse_search_response(search_response: dict,
                           search_type: Type[SearchType]):
    if search_type == SearchType.ALBUM:
        return [spotify.Album.from_api_response(json.dumps(x)) for x in
                search_response["items"]]
    if search_type == SearchType.ARTIST:
        return [spotify.Artist.from_api_response(json.dumps(x)) for x in
                search_response["items"]]
    if search_type == SearchType.PLAYLIST:
        return [spotify.Playlist.from_api_response(json.dumps(x)) for x in
                search_response["items"]]
    if search_type == SearchType.TRACK:
        return [spotify.Track.from_api_response(json.dumps(x)) for x in
                search_response["items"]]


def search(search_term: str, token: str, search_result_count: int = 5,
           search_type: Type[SearchType] = SearchType.TRACK) \
        -> List[typing.Union[
            "spotify.Album", "spotify.Artist", "spotify.Playlist", "spotify" \
                                                                   ".Track"]]:
    if search_type in [SearchType.SHOW, SearchType.EPISODE]:
        raise NotImplemented
    response: dict = json.loads(
        get_request_sync(
            url=BASE_URL.format(urllib.parse.quote(search_term), search_type,
                                search_result_count),
            extra_headers=build_auth_header(token)
        )
    )
    return _parse_search_response(response, search_type)


async def search_async(search_term: str, token: str, search_result_count: int,
                       search_type: Type[SearchType] = SearchType.TRACK) \
        -> List["spotify.Track"]:
    if search_type in [SearchType.SHOW, SearchType.EPISODE]:
        raise NotImplemented
    response: dict = json.loads(
        await get_request_async(
            url=BASE_URL.format(urllib.parse.quote(search_term), search_type,
                                search_result_count),
            extra_headers=build_auth_header(token)
        )
    )
    return _parse_search_response(response, search_type)
