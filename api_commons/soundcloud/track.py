import json
from dataclasses import dataclass
from typing import Optional, List

import api_commons.soundcloud as soundcloud
from api_commons.soundcloud.support_classes import Visual, Stream
from api_commons.soundcloud.user import User
from api_commons.common.utils import has_aiohttp
from .utils import (
    resolve_url,
    resolve_transcoding,
    resolve_url_async,
    resolve_transcoding_async,
    extract_visuals,
)


@dataclass
class Track:
    """
    Dataclass for SoundCloud Songs / Tracks.
    """

    comment_count: int
    """Number of comments under the Track."""
    full_duration: int
    """Duration of the Track in milliseconds."""
    downloadable: bool
    """True if the Track is downloadable directly from the Tracks page"""
    created_at: str
    """Date on which the Track was uploaded to SoundCloud"""
    description: str
    """Song description on the Tracks page"""
    title: str
    """Song title of the Track."""
    duration: int
    """See Track.full_duration"""
    artwork_url: str
    """Url to to the Tracks artwork / album art."""
    tag_list: str
    """Comma separated list of tags. May be empty."""
    genre: str
    """Genre of the song. May be empty."""
    id: int
    """SoundCloud internal id of the Track."""
    reposts_count: int
    """Number of reposts by other users."""
    label_name: Optional[str]
    """Name of the label associated with the artist. Empty if artist is 
    independent."""
    last_modified: str
    """Date on which the Track was modified."""
    commentable: bool
    """True if a User can leave comments on the Track."""
    visuals: List[Visual]
    """List of Visuals associated with the Track."""
    uri: str
    """SoundCloud intern api endpoint associated with the Track."""
    download_count: int
    """Number of downloads."""
    likes_count: int
    """Number of likes."""
    urn: str
    """SoundCloud intern uniform resource name for the Track."""
    license: str
    """License under which the Track is licensed to SoundCloud."""
    display_date: str
    release_date: Optional[str]
    waveform_url: str
    permalink: str
    permalink_url: str
    user: User
    playback_count: int
    streams: List[Stream]

    @classmethod
    def from_api_response(cls, api_response: str) -> "Track":
        """Parses a soundcloud api response into a track.

        Args:
            api_response: api_response from soundcloud servers

        Returns:
            A Track object with all attributes in the api_response

        """
        parsed_api_response: dict = json.loads(api_response)
        if len(parsed_api_response.keys()) == 4:
            return None
        return cls(
            comment_count=parsed_api_response["comment_count"],
            full_duration=parsed_api_response.get("full_duration", None),
            downloadable=parsed_api_response.get("downloadable", None),
            created_at=parsed_api_response["created_at"],
            description=parsed_api_response["description"],
            title=parsed_api_response["title"],
            duration=parsed_api_response["duration"],
            artwork_url=parsed_api_response["artwork_url"],
            tag_list=parsed_api_response["tag_list"],
            genre=parsed_api_response["genre"],
            id=parsed_api_response["id"],
            reposts_count=parsed_api_response["reposts_count"],
            label_name=parsed_api_response["label_name"],
            last_modified=parsed_api_response["last_modified"],
            commentable=parsed_api_response["commentable"],
            uri=parsed_api_response["uri"],
            download_count=parsed_api_response["download_count"],
            likes_count=parsed_api_response["likes_count"],
            urn=parsed_api_response["urn"],
            license=parsed_api_response["license"],
            display_date=parsed_api_response["display_date"],
            release_date=parsed_api_response["release_date"],
            waveform_url=parsed_api_response["waveform_url"],
            permalink=parsed_api_response["permalink"],
            permalink_url=parsed_api_response["permalink_url"],
            user=soundcloud.User.from_api_response(
                json.dumps(parsed_api_response["user"])
            ),
            playback_count=parsed_api_response["playback_count"],
            visuals=extract_visuals(parsed_api_response),
            streams=[
                soundcloud.Stream.from_api_response(json.dumps(x))
                for x in parsed_api_response["transcodings"]
            ]
            if "transcodings" in parsed_api_response
            else None,
        )

    @staticmethod
    def get_by_url(track_url: str, token: str) -> "Track":
        resolve_data = resolve_url(track_url, token)
        data = json.loads(resolve_data)
        data["transcodings"] = []
        # resolve the streaming data
        for transcoding in data["media"]["transcodings"]:
            transcoding = resolve_transcoding(
                transcoding=transcoding, token=token
            )
            data["transcodings"].append(transcoding)
        return Track.from_api_response(json.dumps(data))

    @staticmethod
    @has_aiohttp
    async def get_by_url_async(track_url: str, token: str) -> "Track":
        resolve_data = await resolve_url_async(track_url, token)
        data = json.loads(resolve_data)
        data["transcodings"] = []
        # resolve the streaming data
        for transcoding in data["media"]["transcodings"]:
            transcoding = await resolve_transcoding_async(
                transcoding=transcoding, token=token
            )
            data["transcodings"].append(transcoding)
        return Track.from_api_response(json.dumps(data))
