from dataclasses import dataclass
import json
import spotify

from typing import List, Optional

from common.error import IncompleteObjectError
from common.utils import has_aiohttp
from common.web import get_request_sync, get_request_async
from spotify import ExternalUrls, Image
from spotify.utils import build_auth_header


@dataclass
class Artist:
    external_urls: ExternalUrls
    followers: Optional[int]
    genres: Optional[List[str]]
    endpoint: str
    id: str
    images: Optional[List[Image]]
    name: str
    popularity: Optional[int]
    uri: str
    top_tracks: List["spotify.Track"] = None
    albums: List["spotify.Album"] = None

    @classmethod
    def from_api_response(cls, api_response: str) -> "Artist":
        parsed_api_response = json.loads(api_response)
        return cls(
            external_urls=ExternalUrls.from_api_response(
                json.dumps(parsed_api_response["external_urls"])
            ),
            followers=parsed_api_response["followers"]["total"]
            if "followers" in parsed_api_response
            else None,
            genres=parsed_api_response["genres"]
            if "genres" in parsed_api_response
            else None,
            endpoint=parsed_api_response["href"],
            id=parsed_api_response["id"],
            images=[
                Image.from_api_response(json.dumps(x))
                for x in parsed_api_response["images"]
            ]
            if "images" in parsed_api_response
            else None,
            name=parsed_api_response["name"],
            popularity=parsed_api_response["popularity"]
            if "popularity" in parsed_api_response
            else None,
            uri=parsed_api_response["uri"],
        )

    @staticmethod
    def from_id(artist_id: str, token: str):
        url = f"https://api.spotify.com/v1/artist/{artist_id}"
        return Artist.from_api_response(
            get_request_sync(
                url=url, extra_headers=build_auth_header(token=token)
            )
        )

    @staticmethod
    @has_aiohttp
    async def from_id_async(artist_id: str, token: str):
        url = f"https://api.spotify.com/v1/artist/{artist_id}"
        return Artist.from_api_response(
            await get_request_async(
                url=url, extra_headers=build_auth_header(token)
            )
        )

    def complete(self, token: str) -> "Artist":
        if None not in self.__dict__.values():
            return self
        if not self.id:
            raise IncompleteObjectError
        return Artist.from_id(self.id, token)

    @has_aiohttp
    async def complete_async(self, token: str) -> "Artist":
        if None not in self.__dict__.values():
            return self
        if not self.id:
            raise IncompleteObjectError
        return await Artist.from_id_async(self.id, token)

    @staticmethod
    def get_top_tracks_by_id(artist_id: str, token: str):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        parsed_response: dict = json.loads(
            get_request_sync(url, extra_headers=build_auth_header(token=token))
        )
        return [
            spotify.Track.from_api_response(json.dumps(x))
            for x in parsed_response["tracks"]
        ]

    @staticmethod
    @has_aiohttp
    async def get_top_tracks_by_id_async(artist_id: str, token: str):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        parsed_response: dict = json.loads(
            await get_request_async(
                url, extra_headers=build_auth_header(token=token)
            )
        )
        return [
            spotify.Track.from_api_response(json.dumps(x))
            for x in parsed_response["tracks"]
        ]

    def get_top_tracks(self, token: str):
        if self.top_tracks:
            return self.top_tracks
        if not self.id:
            raise IncompleteObjectError
        self.top_tracks = Artist.get_top_tracks_by_id(self.id, token)
        return self.top_tracks

    @has_aiohttp
    async def get_top_tracks_async(self, token: str):
        if self.top_tracks:
            return self.top_tracks
        if not self.id:
            raise IncompleteObjectError
        self.top_tracks = await Artist.get_top_tracks_by_id_async(
            self.id, token
        )
        return self.top_tracks

    @staticmethod
    def get_albums_by_id(artist_id: str, token: str):
        url: str = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        parsed_response: dict = json.loads(
            get_request_sync(url, extra_headers=build_auth_header(token))
        )
        return [
            spotify.Album.from_api_response(json.dumps(x))
            for x in parsed_response["items"]
        ]

    @staticmethod
    @has_aiohttp
    async def get_albums_by_id_async(artist_id: str, token: str):
        url: str = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        parsed_response: dict = json.loads(
            await get_request_async(url, extra_headers=build_auth_header(token))
        )
        return [
            spotify.Album.from_api_response(json.dumps(x))
            for x in parsed_response["items"]
        ]

    def get_albums(self, token: str):
        if self.albums:
            return self.albums
        if not self.id:
            raise IncompleteObjectError
        self.albums = Artist.get_albums_by_id(self.id, token)
        return self.albums

    @has_aiohttp
    async def get_albums_async(self, token: str):
        if self.albums:
            return self.albums
        if not self.id:
            raise IncompleteObjectError
        self.albums = await Artist.get_albums_by_id_async(self.id, token)
        return self.albums
