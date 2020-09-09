import json
from dataclasses import dataclass

from typing import List, Optional

import api_commons.spotify as spotify
from api_commons.common.error import IncompleteObjectError
from api_commons.common.utils import has_aiohttp
from api_commons.common.web import get_request_async, get_request_sync
from .utils import build_auth_header


@dataclass
class Playlist:
    collaborative: bool
    description: str
    external_urls: "spotify.ExternalUrls"
    followers: Optional[int]
    endpoint: str
    id: str
    images: List["spotify.Image"]
    name: str
    owner: "spotify.User"
    public: Optional[bool]
    snapshot_id: str
    tracks: Optional[List["spotify.Track"]]
    uri: str

    @classmethod
    def from_api_response(cls, api_response: str) -> "Playlist":
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            collaborative=parsed_api_response["collaborative"],
            description=parsed_api_response["description"],
            external_urls=spotify.ExternalUrls.from_api_response(
                json.dumps(parsed_api_response["external_urls"])
            ),
            followers=parsed_api_response["followers"]["total"]
            if "followers" in parsed_api_response
            else None,
            endpoint=parsed_api_response["href"],
            id=parsed_api_response["id"],
            images=[
                spotify.Image.from_api_response(json.dumps(x))
                for x in parsed_api_response["images"]
            ],
            name=parsed_api_response["name"],
            owner=spotify.User.from_api_response(
                json.dumps(parsed_api_response["owner"])
            ),
            public=parsed_api_response["public"],
            snapshot_id=parsed_api_response["snapshot_id"],
            tracks=[
                spotify.Track.from_api_response(json.dumps(x["track"]))
                for x in parsed_api_response["tracks"]["items"]
            ]
            if "items" in parsed_api_response["tracks"]
            else None,
            uri=parsed_api_response["uri"],
        )

    @staticmethod
    def from_id(playlist_id: str, token: str):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        response: str = get_request_sync(
            url=url, extra_headers=build_auth_header(token=token)
        )
        parsed_response: dict = json.loads(response)
        copied_parsed_response: dict = dict(parsed_response)

        while (
            copied_parsed_response["tracks"]["next"]
            if "tracks" in copied_parsed_response
            else copied_parsed_response["next"]
        ):
            response: str = get_request_sync(
                url=copied_parsed_response["tracks"]["next"]
                if "tracks" in copied_parsed_response
                else copied_parsed_response["next"],
                extra_headers=build_auth_header(token=token),
            )
            copied_parsed_response = json.loads(response)
            parsed_response["tracks"]["items"].extend(
                copied_parsed_response["items"]
            )

        return Playlist.from_api_response(json.dumps(parsed_response))

    @staticmethod
    @has_aiohttp
    async def from_id_async(playlist_id: str, token: str):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        response: str = await get_request_async(
            url=url, extra_headers=build_auth_header(token=token)
        )
        parsed_response: dict = json.loads(response)
        copied_parsed_response: dict = dict(parsed_response)

        while (
            copied_parsed_response["tracks"]["next"]
            if "tracks" in copied_parsed_response
            else copied_parsed_response["next"]
        ):
            response: str = await get_request_async(
                url=copied_parsed_response["tracks"]["next"]
                if "tracks" in copied_parsed_response
                else copied_parsed_response["next"],
                extra_headers=build_auth_header(token=token),
            )
            copied_parsed_response = json.loads(response)
            parsed_response["tracks"]["items"].extend(
                copied_parsed_response["items"]
            )

        return Playlist.from_api_response(json.dumps(parsed_response))

    def complete(self, token: str) -> "Playlist":
        if None not in self.__dict__.values():
            return self
        if not self.id:
            raise IncompleteObjectError
        return Playlist.from_id(self.id, token)

    @has_aiohttp
    async def complete_async(self, token: str) -> "Playlist":
        if None not in self.__dict__.values():
            return self
        if not self.id:
            raise IncompleteObjectError
        return await Playlist.from_id_async(self.id, token)
