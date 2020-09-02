import json
from dataclasses import dataclass
from typing import Optional, List

import api_commons.genius as genius
from api_commons.genius.utils import extract_text


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
            **{
                k: v
                for k, v in parsed_api_response.items()
                if k in cls.__annotations__.keys()
            }
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
            **{
                k: v
                for k, v in parsed_api_response.items()
                if k in cls.__annotations__.keys()
            }
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
            **{
                k: v
                for k, v in parsed_api_response.items()
                if k in cls.__annotations__.keys()
            }
        )


@dataclass
class Lyric:
    text: str
    annotation_id: Optional[int] = None
    annotation: Optional[str] = None

    def put_annotation(self, annotation: dict):
        self.annotation = extract_text(
            annotation["annotations"][0]["body"]["dom"]
        )

    @classmethod
    def from_api_response(cls, raw_api_response: str) -> "genius.Lyric":
        if not raw_api_response.startswith("{"):
            return cls(json.loads(raw_api_response).strip())
        parsed_api_response: dict = json.loads(raw_api_response)
        return cls(
            text=extract_text(parsed_api_response).strip(),
            annotation_id=int(parsed_api_response["data"]["id"])
            if "data" in parsed_api_response
            else None,
        )


@dataclass
class Line:
    parts: List[Lyric]

    @property
    def text(self):
        return "".join(map(lambda part: part.text, self.parts))

    @classmethod
    def from_api_response(cls, raw_api_response: str) -> "Line":
        return cls(

            [
                Lyric.from_api_response(json.dumps(x)) for x in
                json.loads(raw_api_response)
            ]
        )


@dataclass
class LyricsBlock:
    lyrics: List[Line]

    @property
    def lyrics_str(self):
        return "\n".join(map(lambda item: item.text, self.lyrics))

    @classmethod
    def from_api_response(cls, raw_api_response: str):
        parsed_api_response: list = json.loads(raw_api_response)
        raw_lines = []
        temp = []
        for part in parsed_api_response:
            if part == "\n":
                raw_lines.append(temp)
                temp = []
                continue
            temp.append(part)
        raw_lines.append(temp)
        raw_lines = list(filter(
            lambda item: item != [],
            raw_lines
        ))
        return cls(
            [
                Line.from_api_response(json.dumps(x))
                for x in raw_lines
            ]
        )
