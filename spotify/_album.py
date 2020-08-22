import json
from dataclasses import dataclass

from typing import List, Optional

import spotify
from common.error import IncompleteObjectError
from common.web import get_request_sync, get_request_async
from spotify.utils import build_auth_header, extract_track_list


@dataclass
class Album:
    album_type: str
    artists: Optional[List["spotify.Artist"]]
    available_markets: List[str]
    copyrights: Optional[List["spotify.Copyright"]]
    external_ids: Optional["spotify.ExternalIds"]
    external_urls: "spotify.ExternalUrls"
    genres: Optional[List[str]]
    endpoint: str
    id: str
    images: List[spotify.Image]
    label: Optional[str]
    name: str
    popularity: Optional[int]
    release_date: Optional[str]
    release_date_precision: Optional[str]
    tracks: Optional[List["spotify.Track"]]
    uri: str

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response = json.loads(api_response)
        return cls(
            album_type=parsed_api_response["album_type"],
            artists=[spotify.Artist.from_api_response(json.dumps(x)) for x in
                     parsed_api_response[
                         "artists"]] if "artists" in parsed_api_response else
            None,
            available_markets=parsed_api_response["available_markets"],
            copyrights=[spotify.Copyright.from_api_response(json.dumps(x)) for x
                        in
                        parsed_api_response[
                            "copyrights"]] if "copyrights" in
                                              parsed_api_response else None,
            external_ids=spotify.ExternalIds.from_api_response(
                json.dumps(parsed_api_response[
                               "external_ids"])) if "external_ids" in
                                                    parsed_api_response else
            None,
            external_urls=spotify.ExternalUrls.from_api_response(
                json.dumps(parsed_api_response["external_urls"])
            ),
            genres=parsed_api_response[
                "genres"] if "genres" in parsed_api_response else None,
            endpoint=parsed_api_response["href"],
            id=parsed_api_response["id"],
            images=[spotify.Image.from_api_response(json.dumps(x)) for x in
                    parsed_api_response["images"]],
            label=parsed_api_response[
                "label"] if "label" in parsed_api_response else None,
            name=parsed_api_response["name"],
            popularity=parsed_api_response[
                "popularity"] if "popularity" in parsed_api_response else None,
            release_date=parsed_api_response[
                "release_date"] if "release_date" in parsed_api_response else
            None,
            release_date_precision=parsed_api_response[
                "release_date_precision"] if "release_date_precision" in
                                             parsed_api_response else None,
            tracks=extract_track_list(parsed_api_response),
            uri=parsed_api_response["uri"]
        )

    @staticmethod
    def from_id(artist_id: str, token: str):
        url = f"https://api.spotify.com/v1/albums/{artist_id}"
        return Album.from_api_response(
            get_request_sync(url=url,
                             extra_headers=build_auth_header(
                                 token=token)))

    @staticmethod
    async def from_id_async(artist_id: str, token: str):
        url = f"https://api.spotify.com/v1/albums/{artist_id}"
        return Album.from_api_response(
            await get_request_async(url=url,
                                    extra_headers=build_auth_header(
                                        token)))

    def complete(self, token: str) -> "Album":
        if None not in self.__dict__.values():
            return self
        if not self.id:
            raise IncompleteObjectError
        return Album.from_id(self.id, token)

    async def complete_async(self, token: str) -> "Album":
        if None not in self.__dict__.values():
            return self
        if not self.id:
            raise IncompleteObjectError
        return await Album.from_id_async(self.id, token)
