from dataclasses import dataclass

import json
from typing import List, Optional

from common.error import IncompleteObjectError
from common.utils import has_aiohttp
from common.web import get_request_sync, get_request_async
from spotify.album import Album
from spotify.artist import Artist
from spotify.support_classes import ExternalIds, ExternalUrls
from spotify.utils import build_auth_header


@dataclass
class Track:
    album: Album
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    track_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIds
    external_urls: ExternalUrls
    endpoint: str
    id: str
    name: str
    popularity: int
    preview_url: Optional[str]
    uri: str

    @classmethod
    def from_api_response(cls, api_response: str) -> "Track":
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            album=Album.from_api_response(
                json.dumps(parsed_api_response["album"])
            ),
            artists=[
                Artist.from_api_response(json.dumps(x))
                for x in parsed_api_response["artists"]
            ],
            available_markets=parsed_api_response["available_markets"],
            disc_number=parsed_api_response["disc_number"],
            track_number=parsed_api_response["track_number"],
            duration_ms=parsed_api_response["duration_ms"],
            explicit=parsed_api_response["explicit"],
            external_ids=ExternalIds.from_api_response(
                json.dumps(parsed_api_response["external_ids"])
            ),
            external_urls=ExternalUrls.from_api_response(
                json.dumps(parsed_api_response["external_urls"])
            ),
            endpoint=parsed_api_response["href"],
            id=parsed_api_response["id"],
            name=parsed_api_response["name"],
            popularity=parsed_api_response["popularity"],
            preview_url=parsed_api_response["preview_url"],
            uri=parsed_api_response["uri"],
        )

    @staticmethod
    def from_id(track_id: str, token: str) -> "Track":
        return Track.from_api_response(
            get_request_sync(
                url=f"https://api.spotify.com/v1/tracks/{track_id}",
                extra_headers=build_auth_header(token=token),
            )
        )

    @staticmethod
    @has_aiohttp
    async def from_id_async(track_id: str, token: str) -> "Track":
        return Track.from_api_response(
            await get_request_async(
                url=f"https://api.spotify.com/v1/tracks/{track_id}",
                extra_headers=build_auth_header(token=token),
            )
        )

    def complete(self, token: str) -> "Track":
        if None not in self.__dict__.values():
            return self
        if not self.id:
            raise IncompleteObjectError
        return Album.from_id(self.id, token)

    @has_aiohttp
    async def complete_async(self, token: str) -> "Track":
        if None not in self.__dict__.values():
            return self
        if not self.id:
            raise IncompleteObjectError
        return await Album.from_id_async(self.id, token)
