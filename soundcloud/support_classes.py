import json
from dataclasses import dataclass
from enum import Enum

from typing import Type


@dataclass
class Visual:
    urn: str
    visual_url: str
    entry_time: int

    @classmethod
    def from_api_response(cls, api_response: str) -> "Visual":
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            urn=parsed_api_response["urn"],
            visual_url=parsed_api_response["visual_url"],
            entry_time=parsed_api_response["entry_time"],
        )


@dataclass
class Stream:
    url: str
    duration: int
    quality: str
    format: "Format"

    @classmethod
    def from_api_response(cls, api_response: str) -> "Stream":
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            url=parsed_api_response["url"],
            duration=parsed_api_response["duration"],
            quality=parsed_api_response["quality"],
            format=Format.from_api_response(
                json.dumps(parsed_api_response["format"])
            ),
        )


class Codec(Enum):
    OPUS = 1
    MP3 = 2


@dataclass
class Format:
    protocol: str
    codec: Codec

    @classmethod
    def from_api_response(cls, api_response: str) -> "Format":
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            protocol=parsed_api_response["protocol"],
            codec=Codec.OPUS
            if "opus" in parsed_api_response["mime_type"]
            else Codec.MP3,
        )
