import json
from dataclasses import dataclass
from typing import Optional, List

import api_commons.genius as genius
from api_commons.common.utils import get_recursively
from api_commons.genius.utils import (
    extract_text,
    get_album_tracks,
    get_album_tracks_async,
)


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
    tracks: Optional[List["genius.Lyrics"]] = None

    def get_tracks(self) -> List["genius.Lyrics"]:
        if not self.tracks:
            self.tracks = get_album_tracks(self.id)
        return self.tracks

    async def get_tracks_async(self):
        if not self.tracks:
            self.tracks = await get_album_tracks_async(self.id)
        return self.tracks

    @classmethod
    def from_api_response(cls, raw_api_response: str):
        parsed_api_response: dict = json.loads(raw_api_response)
        parsed_api_response["artist"] = Artist.from_api_response(
            json.dumps(parsed_api_response["artist"])
        )
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
    instagram_name: Optional[str] = None
    twitter_name: Optional[str] = None

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
    _referenced_urls: List[str] = None
    annotation_id: Optional[str] = None
    annotation: Optional[str] = None
    link: Optional[str] = None

    @property
    def is_dummy(self):
        return self.text == '' and self._referenced_urls is None and \
               self.annotation_id is None and self.annotation is None and \
               self.link is None

    @property
    def referenced_urls(self):
        return self._referenced_urls or []

    def put_annotation(self, annotation: dict):
        self.annotation = extract_text(
            annotation["annotations"][0]["body"]["dom"]
        )
        self._referenced_urls = list(
            map(
                lambda item: item["attributes"]["href"],
                get_recursively(
                    annotation["annotations"][0]["body"]["dom"], "tag", "a"
                ),
            )
        )

    @classmethod
    def from_api_response(cls, raw_api_response: str) -> "genius.Lyric":
        if not raw_api_response.startswith("{"):
            return cls(json.loads(raw_api_response))
        parsed_api_response: dict = json.loads(raw_api_response)
        lnk: Optional[str] = None
        if parsed_api_response["tag"] == "a":
            lnk = parsed_api_response["attributes"]["href"]

        return cls(
            text=extract_text(parsed_api_response),
            annotation_id=parsed_api_response["data"].get("id", None)
            if "data" in parsed_api_response
            else None,
            link=lnk,
        )


@dataclass
class Line:
    parts: List[Lyric]

    @property
    def referenced_urls(self):
        r_urls = []
        for reference in self.parts:
            r_urls.extend(reference.referenced_urls)
        return r_urls

    @property
    def text(self):
        return "".join(map(lambda part: part.text, self.parts))

    @classmethod
    def from_api_response(cls, raw_api_response: str) -> "Line":
        return cls(
            list(
                filter(
                    lambda x: not x.is_dummy,
                    [
                        Lyric.from_api_response(json.dumps(x))
                        for x in json.loads(raw_api_response)
                    ]
                )
            )
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
            if part == "\n" or (
                (
                    part.get("tag", None)
                    if isinstance(part, dict)
                    else None
                ) in ["h1", "h2", "h3", "h4"]
            ):
                if isinstance(part, dict):
                    temp.append(part)
                raw_lines.append(temp)
                temp = []
                continue
            temp.append(part)
        raw_lines.append(temp)
        raw_lines = list(filter(lambda item: item != [], raw_lines))
        return cls([Line.from_api_response(json.dumps(x)) for x in raw_lines])


@dataclass
class Tag:
    name: str
    primary: bool
    id: int
    url: str

    @classmethod
    def from_api_response(cls, raw_api_response: str):
        return cls(
            **{
                k: v
                for k, v in json.loads(raw_api_response).items()
                if k in cls.__annotations__.keys()
            }
        )
