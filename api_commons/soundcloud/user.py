import json
from dataclasses import dataclass
from typing import Optional, List
import api_commons.soundcloud as soundcloud
from .utils import extract_visuals


@dataclass
class User:
    avatar_url: str
    city: str
    comments_count: Optional[int]
    country_code: str
    created_at: Optional[str]
    description: Optional[str]
    followers_count: Optional[int]
    followings_count: Optional[int]
    first_name: str
    full_name: str
    groups_count: Optional[int]
    id: int
    last_modified: str
    last_name: str
    likes_count: Optional[int]
    playlist_likes_count: Optional[int]
    permalink: str
    permalink_url: str
    playlist_count: Optional[int]
    reposts_count: Optional[int]
    track_count: Optional[int]
    uri: str
    urn: str
    username: str
    verified: bool
    visuals: List["soundcloud.Visual"]

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            avatar_url=parsed_api_response["avatar_url"],
            city=parsed_api_response["city"],
            comments_count=parsed_api_response.get("comments_count", None),
            country_code=parsed_api_response["country_code"],
            created_at=parsed_api_response.get("created_at", None),
            description=parsed_api_response.get("description", None),
            followers_count=parsed_api_response.get("followers_count", None),
            followings_count=parsed_api_response.get("followings_count", None),
            first_name=parsed_api_response["first_name"],
            full_name=parsed_api_response["full_name"],
            groups_count=parsed_api_response.get("groups_count", None),
            id=parsed_api_response["id"],
            last_modified=parsed_api_response["last_modified"],
            last_name=parsed_api_response["last_name"],
            likes_count=parsed_api_response.get("likes_count", None),
            playlist_likes_count=parsed_api_response.get(
                "playlist_likes_count", None
            ),
            permalink=parsed_api_response["permalink"],
            permalink_url=parsed_api_response["permalink_url"],
            playlist_count=parsed_api_response.get("playlist_count", None),
            reposts_count=parsed_api_response.get("reposts_count", None),
            track_count=parsed_api_response.get("track_count", None),
            uri=parsed_api_response["uri"],
            urn=parsed_api_response["urn"],
            username=parsed_api_response["username"],
            verified=parsed_api_response["verified"],
            visuals=extract_visuals(parsed_api_response),
        )
