import json
from dataclasses import dataclass

from typing import List

import genius
from genius.utils import (
    request_id,
    request_id_async,
    parse_lyrics,
    request_referents,
    parse_referents,
    request_referents_async,
)


@dataclass
class Lyrics:
    annotation_count: int
    full_title: str
    header_image_url: str
    id: int
    instrumental: bool
    lyrics_owner_id: int
    lyrics_state: str
    lyrics_updated_at: int
    path: str
    song_art_image_url: str
    stats: "genius.Stats"
    title: str
    title_with_featured: str
    url: str
    album: "genius.Album"
    primary_artist: "genius.Artist"
    featured_artists: List["genius.Artist"]
    comment_count: int
    custom_header_image_url: str
    custom_song_art_image_url: str
    description: str
    is_music: bool
    lyrics: List["genius.LyricsBlock"]
    release_date: str
    share_url: str

    @staticmethod
    def get_by_id(song_id: str) -> "genius.Lyrics":
        return Lyrics.from_api_response(request_id(song_id=song_id))

    @staticmethod
    async def get_by_id_async(song_id: str) -> "genius.Lyrics":
        return Lyrics.from_api_response(await request_id_async(song_id=song_id))

    @property
    def annotation_ids(self) -> List[str]:
        ids = []
        for lb in self.lyrics:
            for ly in lb.lyrics:
                if ly.annotation_id:
                    ids.append(str(ly.annotation_id))
        return ids

    def _put_annotation(self, annotation_id: str, annotation: dict) -> None:
        for lb in self.lyrics:
            for ly in lb.lyrics:
                if ly.annotation_id == int(annotation_id):
                    ly.put_annotation(annotation)

    def _put_annotations(self, annotations: dict):
        for k in annotations:
            self._put_annotation(k, annotations[k])

    def load_annotations(self) -> None:
        self._put_annotations(
            parse_referents(request_referents(self.annotation_ids))
        )

    async def load_annotations_async(self) -> None:
        self._put_annotations(
            parse_referents(await request_referents_async(self.annotation_ids))
        )

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)
        if "response" in parsed_api_response:
            parsed_api_response = parsed_api_response["response"]["song"]

        parsed_api_response["stats"] = genius.Stats.from_api_response(
            json.dumps(parsed_api_response["stats"])
        )
        parsed_api_response["album"] = (
            genius.Album.from_api_response(
                json.dumps(parsed_api_response["album"])
            )
            if "album" in parsed_api_response
            else None
        )
        parsed_api_response["primary_artist"] = genius.Artist.from_api_response(
            json.dumps(parsed_api_response["primary_artist"])
        )
        parsed_api_response["featured_artists"] = (
            [
                genius.Artist.from_api_response(json.dumps(x))
                for x in parsed_api_response["featured_artists"]
            ]
            if "featured_artists" in parsed_api_response
            else None
        )
        parsed_api_response["lyrics"] = parse_lyrics(
            parsed_api_response["lyrics"]
        )
        return cls(
            **{
                k: v
                for k, v in parsed_api_response.items()
                if k in cls.__annotations__.keys()
            }
        )

    @property
    def lyrics_str(self) -> str:
        return "\n\n".join(map(lambda item: item.lyrics_str, self.lyrics))
