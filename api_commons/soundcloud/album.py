import json
from dataclasses import dataclass

from typing import List

import api_commons


@dataclass
class Album:
    artwork_url: str
    created_at: str
    description: str
    display_date: str
    duration: int
    genre: str
    id: str
    label_name: str
    last_modified: str
    license: str
    likes_count: int
    managed_by_feeds: bool
    permalink: str
    permalink_url: str
    public: bool
    published_at: str
    purchase_title: str
    purchase_url: str
    release_date: str
    reposts_count: int
    title: str
    tracks: List["api_commons.soundcloud.Track"]
    uri: str
    user: "api_commons.soundcloud.User"

    @classmethod
    def from_api_response(cls, raw_api_response):
        parsed_api_response: dict = json.loads(raw_api_response)
        parsed_api_response["tracks"] = [
            api_commons.soundcloud.Track.from_api_response(json.dumps(x))
            for x in parsed_api_response["tracks"]
        ]
        parsed_api_response[
            "user"] = api_commons.soundcloud.User.from_api_response(
            json.dumps(parsed_api_response["user"]))

        return cls(
            **{
                k: v
                for k, v in parsed_api_response.items()
                if k in cls.__annotations__.keys()
            }
        )
