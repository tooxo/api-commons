import json
from dataclasses import dataclass
from typing import Optional, List

import api_commons.soundcloud as soundcloud
from api_commons.common.utils import has_aiohttp
from .utils import (
    resolve_url,
    get_missing_ids,
    fulfill_missing_requests,
    resolve_url_async,
    fulfill_missing_requests_async,
)


@dataclass
class Set:
    duration: int
    permalink_url: str
    reposts_count: int
    genre: Optional[str]
    permalink: str
    description: Optional[str]
    uri: str
    label_name: Optional[str]
    tag_list: str
    last_modified: str
    license: str
    tracks: List["soundcloud.Track"]
    id: int
    release_date: Optional[str]
    display_date: str
    created_at: str
    likes_count: int
    title: str
    artwork_url: Optional[str]
    is_album: bool
    user: "soundcloud.User"
    published_at: str

    @classmethod
    def from_api_response(cls, api_response: str) -> "Set":
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            duration=parsed_api_response["duration"],
            permalink_url=parsed_api_response["permalink_url"],
            reposts_count=parsed_api_response["reposts_count"],
            genre=parsed_api_response["genre"],
            permalink=parsed_api_response["permalink"],
            description=parsed_api_response["description"],
            uri=parsed_api_response["uri"],
            label_name=parsed_api_response["label_name"],
            tag_list=parsed_api_response["tag_list"],
            last_modified=parsed_api_response["last_modified"],
            license=parsed_api_response["license"],
            tracks=[
                soundcloud.Track.from_api_response(json.dumps(x))
                for x in parsed_api_response["tracks"]
            ],
            id=parsed_api_response["id"],
            release_date=parsed_api_response["release_date"],
            display_date=parsed_api_response["display_date"],
            created_at=parsed_api_response["created_at"],
            likes_count=parsed_api_response["likes_count"],
            title=parsed_api_response["title"],
            artwork_url=parsed_api_response["artwork_url"],
            is_album=parsed_api_response["is_album"],
            user=soundcloud.User.from_api_response(
                json.dumps(parsed_api_response["user"])
            ),
            published_at=parsed_api_response["published_at"],
        )

    @staticmethod
    def get_from_url(
        playlist_url: str, token: str, flat: bool = False
    ) -> "Set":
        playlist_data = resolve_url(url=playlist_url, token=token)
        parsed_set_data: dict = json.loads(playlist_data)
        missing_ids: List[str] = get_missing_ids(parsed_set_data)
        parsed_set_data["tracks"] = list(
            filter(lambda item: "title" in item, parsed_set_data["tracks"])
        )
        if not flat:
            missing_tracks = fulfill_missing_requests(
                missing_ids=missing_ids, token=token
            )
            parsed_set_data["tracks"].extend(missing_tracks)
        return Set.from_api_response(json.dumps(parsed_set_data))

    @staticmethod
    @has_aiohttp
    async def get_from_url_async(
        playlist_url: str, token: str, flat: bool = False
    ) -> "Set":
        playlist_data = await resolve_url_async(url=playlist_url, token=token)
        parsed_set_data: dict = json.loads(playlist_data)
        missing_ids: List[str] = get_missing_ids(parsed_set_data)
        missing_tracks = await fulfill_missing_requests_async(
            missing_ids=missing_ids, token=token
        )
        if not flat:
            parsed_set_data["tracks"] = list(
                filter(lambda item: "title" in item, parsed_set_data["tracks"])
            )
            parsed_set_data["tracks"].extend(missing_tracks)
        return Set.from_api_response(json.dumps(parsed_set_data))
