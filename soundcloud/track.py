import json
from dataclasses import dataclass
from typing import Optional, List

import soundcloud
from common.utils import has_aiohttp
from soundcloud.utils import (
    resolve_url,
    resolve_transcoding,
    resolve_url_async,
    resolve_transcoding_async,
    extract_visuals,
)


@dataclass
class Track:
    comment_count: int
    full_duration: int
    downloadable: bool
    created_at: str
    description: str
    title: str
    duration: int
    artwork_url: str
    tag_list: str
    genre: str
    id: int
    reposts_count: int
    label_name: Optional[str]
    last_modified: str
    commentable: bool
    visuals: List["soundcloud.Visual"]
    uri: str
    download_count: int
    likes_count: int
    urn: str
    license: str
    display_date: str
    release_date: Optional[str]
    waveform_url: str
    permalink: str
    permalink_url: str
    user: "soundcloud.User"
    playback_count: int
    streams: List["soundcloud.Stream"]

    @classmethod
    def from_api_response(cls, api_response: str) -> "Track":
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            comment_count=parsed_api_response["comment_count"],
            full_duration=parsed_api_response["full_duration"],
            downloadable=parsed_api_response["downloadable"],
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
