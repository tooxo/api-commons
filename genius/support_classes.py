import json
from dataclasses import dataclass
from typing import Optional

import genius


@dataclass
class Stats:
    unreviewed_annotations: int
    hot: bool
    pageviews: Optional[int] = None
    accepted_annotations: Optional[int] = None
    verified_annotations: Optional[int] = None
    contributors: Optional[int] = None
    iq_earners: Optional[int] = None
    transcribers: Optional[int] = None

    @classmethod
    def from_api_response(cls, raw_api_response: str):
        parsed_api_response: dict = json.loads(raw_api_response)
        return cls(
            **{k: v for k, v in parsed_api_response.items() if
               k in cls.__annotations__.keys()}
        )


@dataclass
class Album:
    cover_art_url: str
    full_title: str
    id: int
    name: str
    name_with_artist: str
    url: str
    artist: "genius.Artist"

    @classmethod
    def from_api_response(cls, raw_api_response: str):
        parsed_api_response: dict = json.loads(raw_api_response)
        return cls(
            **{k: v for k, v in parsed_api_response.items() if
               k in cls.__annotations__.keys()}
        )


@dataclass
class Artist:
    header_image_url: str
    id: int
    image_url: str
    is_verified: bool
    is_meme_verified: bool
    name: str
    slug: str
    url: str
    id: int

    @classmethod
    def from_api_response(cls, raw_api_response: str):
        parsed_api_response: dict = json.loads(raw_api_response)
        return cls(
            **{k: v for k, v in parsed_api_response.items() if
               k in cls.__annotations__.keys()}
        )
