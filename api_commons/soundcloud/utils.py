import json
import re

from typing import List, Optional

import api_commons.soundcloud as soundcloud
from api_commons.common.web import get_request_sync, get_request_async
import urllib.parse

SCRIPT_REGEX = re.compile(
    r"(https://a-v2\.sndcdn\.com/assets/\d{1,4}-[\da-z]+\.js)"
)

ID_REGEX = [
    re.compile(r'client_id:"([a-zA-Z0-9]+)"'),
    re.compile(r'client_id=([A-z0-9]+)&device_id')
]

URL_RESOLVE = "https://api.soundcloud.com/resolve?url={}&client_id={}"

COMMON_HEADERS = {
    "Host": "api-v2.soundcloud.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/70.0.3538.27 Safari/537.36",
    "Accept-Charset": "utf-8",
    "Accept": "text/html,application/xhtml+xml,application/"
              "xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-us,en;q=0.5",
    "Connection": "close",
}

PLAYLIST_PATTERN = re.compile(
    r"https://[a-z-\\]+\.sndcdn.com/media/[\d]+/[\d]+[\S]+"
)

URL_MISSING = "https://api-v2.soundcloud.com/tracks?ids={}&client_id={}"


def extract_scripts_from_main_page(html: str) -> List[str]:
    return re.findall(SCRIPT_REGEX, html)


def extract_token_from_script(js: str) -> Optional[str]:
    for pattern in ID_REGEX:
        results = re.findall(pattern, js)
        if results:
            return results[0]
    return None


def resolve_url(url: str, token: str) -> str:
    return get_request_sync(
        url=URL_RESOLVE.format(url, token), extra_headers=COMMON_HEADERS
    )


def resolve_transcoding(transcoding: dict, token: str) -> dict:
    stream_url = json.loads(
        get_request_sync(
            url=f"{transcoding['url']}?client_id={token}",
            extra_headers=COMMON_HEADERS,
        )
    )["url"]

    if "playlist.m3u8" in stream_url:
        last_playlist_entry: str = re.findall(
            PLAYLIST_PATTERN, get_request_sync(stream_url)
        )[-1]
        stream_url = re.sub(r"/[\d]+/", "/0/", last_playlist_entry)

    transcoding["url"] = stream_url
    return transcoding


async def resolve_url_async(url: str, token: str) -> str:
    return await get_request_async(
        url=URL_RESOLVE.format(url, token), extra_headers=COMMON_HEADERS
    )


async def resolve_transcoding_async(transcoding: dict, token: str) -> dict:
    stream_url = json.loads(
        await get_request_async(
            url=f"{transcoding['url']}?client_id={token}",
            extra_headers=COMMON_HEADERS,
        )
    )["url"]

    if "playlist.m3u8" in stream_url:
        last_playlist_entry: str = re.findall(
            PLAYLIST_PATTERN, await get_request_async(stream_url)
        )[-1]
        stream_url = re.sub(r"/[\d]+/", "/0/", last_playlist_entry)

    transcoding["url"] = stream_url
    return transcoding


def get_missing_ids(playlist_data: dict) -> List[str]:
    return list(
        filter(
            lambda item: item is not None,
            map(
                lambda item: str(item["id"]) if "title" not in item else None,
                playlist_data["tracks"],
            ),
        )
    )


def fulfill_missing_requests(missing_ids: List[str], token: str) -> List[dict]:
    missing_tracks: List[dict] = []
    while missing_ids:
        ids: list = missing_ids[::50]
        del missing_ids[::50]
        missing_tracks.extend(
            json.loads(
                get_request_sync(
                    url=URL_MISSING.format(
                        urllib.parse.quote(",").join(ids), token
                    ),
                )
            )
        )
    return missing_tracks


async def fulfill_missing_requests_async(
    missing_ids: List[str], token: str
) -> List[dict]:
    missing_tracks: List[dict] = []
    while missing_ids:
        ids: list = missing_ids[::50]
        del missing_ids[::50]
        missing_tracks.extend(
            json.loads(
                await get_request_async(
                    url=URL_MISSING.format(
                        urllib.parse.quote(",").join(ids), token
                    ),
                )
            )
        )
    return missing_tracks


def extract_visuals(api_response: dict) -> Optional[List["soundcloud.Visual"]]:
    if "visuals" not in api_response:
        return None
    if not api_response["visuals"]:
        return None
    if "visuals" in api_response["visuals"]:
        return [
            soundcloud.Visual.from_api_response(json.dumps(x))
            for x in api_response["visuals"]["visuals"]
        ]
    return None
