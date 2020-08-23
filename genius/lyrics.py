import json
from dataclasses import dataclass

from typing import List, Optional

import genius


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
    lyrics: str
    release_date: str
    share_url: str

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)

        parsed_api_response["stats"] = genius.Stats.from_api_response(
            json.dumps(parsed_api_response["stats"]))
        parsed_api_response["album"] = genius.Album.from_api_response(
            json.dumps(parsed_api_response[
                           "album"])) if "album" in parsed_api_response else \
            None
        parsed_api_response["primary_artist"] = genius.Artist.from_api_response(
            json.dumps(parsed_api_response["primary_artist"])
        )
        parsed_api_response["featured_artists"] = [
            genius.Artist.from_api_response(json.dumps(x)) for x in
            parsed_api_response[
                "featured_artists"]] if "featured_artists" in \
                                        parsed_api_response else None
        return cls(
            **{k: v for k, v in parsed_api_response.items() if
               k in cls.__annotations__.keys()}
        )
