import json
from dataclasses import dataclass

from typing import List, Optional

import api_commons.genius as genius
from .utils import (
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
    lyrics: Optional[List["genius.LyricsBlock"]]
    comment_count: int = 0
    custom_header_image_url: Optional[str] = None
    custom_song_art_image_url: Optional[str] = None
    description: Optional[str] = None
    is_music: Optional[bool] = None
    release_date: Optional[str] = None
    share_url: Optional[str] = None
    tags: Optional[List["genius.Tag"]] = None
    track_no: Optional[int] = None
    apple_music_id: Optional[int] = None
    youtube_url: Optional[str] = None

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
            for ln in lb.lyrics:
                for ly in ln.parts:
                    if ly.annotation_id:
                        ids.append(str(ly.annotation_id))
        return ids

    def complete_from_id(self):
        new = Lyrics.get_by_id(str(self.id))
        for attr in self.__dict__:
            if hasattr(new, attr) and not getattr(self, attr):
                setattr(self, attr, getattr(new, attr))
        return self

    async def complete_from_id_async(self):
        new = await Lyrics.get_by_id_async(str(self.id))
        for attr in self.__dict__:
            if hasattr(new, attr) and not getattr(self, attr):
                setattr(self, attr, getattr(new, attr))
        return self

    def _put_annotation(self, annotation_id: str, annotation: dict) -> None:
        for lb in self.lyrics:
            for ln in lb.lyrics:
                for ly in ln.parts:
                    if ly.annotation_id == annotation_id:
                        ly.put_annotation(annotation)

    def _put_annotations(self, annotations: dict):
        for k in annotations:
            self._put_annotation(k, annotations[k])

    def load_annotations(self) -> None:
        for smaller_annotation_list in [self.annotation_ids[i:i + 20] for i in
                                        range(0, len(self.annotation_ids), 20)]:
            self._put_annotations(
                parse_referents(request_referents(smaller_annotation_list))
            )

    async def load_annotations_async(self) -> None:
        for smaller_annotation_list in [self.annotation_ids[i:i + 20] for i in
                                        range(0, len(self.annotation_ids), 20)]:
            self._put_annotations(
                parse_referents(
                    await request_referents_async(smaller_annotation_list))
            )

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)
        track_no: Optional[int] = None
        if "song" in parsed_api_response:
            track_no = parsed_api_response["number"] or -1
            parsed_api_response = parsed_api_response["song"]
        if "response" in parsed_api_response:
            parsed_api_response = parsed_api_response["response"]["song"]

        parsed_api_response["stats"] = genius.Stats.from_api_response(
            json.dumps(parsed_api_response["stats"])
        )
        parsed_api_response["album"] = (
            genius.Album.from_api_response(
                json.dumps(parsed_api_response["album"])
            )
            if "album" in parsed_api_response and parsed_api_response["album"]
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
        parsed_api_response["lyrics"] = (
            parse_lyrics(parsed_api_response["lyrics"])
            if "lyrics" in parsed_api_response
            else None
        )
        parsed_api_response["tags"] = [
            genius.Tag.from_api_response(json.dumps(x)) for x in
            parsed_api_response["tags"]
        ] if "tags" in parsed_api_response else None
        parsed_api_response["track_no"] = track_no
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
