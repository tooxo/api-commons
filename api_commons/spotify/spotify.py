import base64
import json
import time
from typing import List, Type

from api_commons.spotify.search import SearchType

import api_commons.spotify as spotify
import api_commons.spotify.validation
from api_commons.common.utils import has_aiohttp
from api_commons.common.web import post_request_sync, post_request_async
from .utils import extract_id


class SpotifyApi:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self._token = None
        self._token_timer = 0

    def get_auth_token(self):
        if self._token and time.time() - self._token_timer < 3540:  # 59 min
            return self._token
        enc = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        )
        token_data = post_request_sync(
            url="https://accounts.spotify.com/api/token",
            payload="grant_type=client_credentials",
            extra_headers={
                "Authorization": f"Basic {enc.decode()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        self._token = json.loads(token_data)["access_token"]
        self._token_timer = time.time()
        return self._token

    @has_aiohttp
    async def get_auth_token_async(self):
        if self._token and time.time() - self._token_timer < 3540:  # 59 min
            return self._token
        enc = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        )
        token_data = await post_request_async(
            url="https://accounts.spotify.com/api/token",
            payload="grant_type=client_credentials",
            extra_headers={
                "Authorization": f"Basic {enc.decode()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        self._token = json.loads(token_data)["access_token"]
        self._token_timer = time.time()
        return self._token

    def search(
            self,
            search_term: str,
            search_result_count: int = 5,
            search_result_offset: int = 0,
            search_type: List[Type[SearchType]] = None,
            include_external: bool = True
    ):
        return spotify.search(search_term, self.get_auth_token(), search_result_count, search_result_offset,
                              search_type, include_external)

    @has_aiohttp
    async def search_async(
            self,
            search_term: str,
            search_result_count: int = 5,
            search_result_offset: int = 0,
            search_type: List[Type[SearchType]] = None,
            include_external: bool = True,
    ):
        return await spotify.search_async(search_term, self.get_auth_token_async(), search_result_count,
                                          search_result_offset,
                                          search_type, include_external)

    @spotify.validation.decorator(spotify.validation.validate_spotify_track)
    def extract_track(self, url: str) -> "spotify.Track":
        return spotify.Track.from_id(extract_id(url=url), self.get_auth_token())

    @has_aiohttp
    @spotify.validation.decorator(spotify.validation.validate_spotify_track)
    async def extract_track_async(self, url: str) -> "spotify.Track":
        return await spotify.Track.from_id_async(
            extract_id(url=url), await self.get_auth_token_async()
        )

    @spotify.validation.decorator(spotify.validation.validate_spotify_playlist)
    def extract_playlist(self, url: str) -> "spotify.Playlist":
        return spotify.Playlist.from_id(
            extract_id(url=url), self.get_auth_token()
        )

    @has_aiohttp
    @spotify.validation.decorator(spotify.validation.validate_spotify_playlist)
    async def extract_playlist_async(self, url: str) -> "spotify.Playlist":
        return await spotify.Playlist.from_id_async(
            extract_id(url=url), await self.get_auth_token_async()
        )
