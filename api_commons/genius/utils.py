import base64

# this genius key was extracted out of the android app via a mitm attack where
# it was sent with every request as a authorization header

# this key is also different from "normal" genius api keys, because the server
# responds with not only the song meta data but also the lyrics and annotations
import json
from typing import List, Union
from urllib.parse import quote

import api_commons.genius as genius
from api_commons.common.web import get_request_sync, get_request_async

GENIUS_SECRET_ENC: str = \
    "VjJ4U2JHRnRPVlZZTWpseFZEQldhR013YkhKV1JHeFlZMnN4UTJGRlNsSlVNMjh5V2xac1RGTjZWbEpXVlhoRVZGVldSR0pWT1c5a2JtUjRZV3hLWVU1c1pHbGpSMFowVW0xVmVsb3lWa2xpYmxwM1RYYzlQUT09"

# this is a simple measure to prevent search engine crawlers from finding this
GENIUS_SECRET: str = base64.b64decode(
    base64.b64decode(base64.b64decode(GENIUS_SECRET_ENC))
).decode()

REFERENCE_HEADERS = {
    "Host": "genius.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
                  "like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}


def build_header() -> dict:
    return {"Authorization": f"Bearer {GENIUS_SECRET}"}


def build_url(song_id) -> str:
    return f"https://api.genius.com/songs/{song_id}"


def request_id(song_id: str) -> str:
    return get_request_sync(
        url=build_url(song_id=song_id), extra_headers=build_header()
    ).replace("\xa0", " ")


async def request_id_async(song_id: str) -> str:
    return (
        await get_request_async(
            url=build_url(song_id=song_id), extra_headers=build_header()
        )
    ).replace("\xa0", " ")


def request_referents(referent_list: List[str]) -> str:
    return get_request_sync(
        url=f"https://genius.com/api/referents/multi?ids="
            f"{quote(','.join(referent_list))}",
        extra_headers=REFERENCE_HEADERS,
    ).replace("\xa0", " ")


async def request_referents_async(referent_list: List[str]) -> str:
    return (
        await get_request_async(
            url=f"https://genius.com/api/referents/multi?ids="
                f"{quote(','.join(referent_list))}",
            extra_headers=REFERENCE_HEADERS,
        )
    ).replace("\xa0", " ")


def parse_referents(referent_response: str) -> dict:
    parsed_reference_response: dict = json.loads(referent_response)
    return parsed_reference_response["response"]["referents"]


def _flatten_lyrics(lyrics_list: List[dict]) -> List[Union[dict, str]]:
    output: List[Union[dict, str]] = []
    for lyr in lyrics_list:
        if isinstance(lyr, dict):
            if lyr["tag"] == "p" and "children" in lyr:
                output.extend(_flatten_lyrics(lyr["children"]))
            else:
                output.append(lyr)
        else:
            output.append(lyr)
    return output


def parse_lyrics(lyrics_catalogue: dict) -> List["genius.LyricsBlock"]:
    if "children" not in lyrics_catalogue["dom"]:
        return []
    lyrics_list: List[Union[str, dict]] = lyrics_catalogue["dom"]["children"]
    if len(lyrics_list) == 1 and "children" in lyrics_list[0]:
        if len(lyrics_list[0]["children"]) > 1:
            lyrics_list = lyrics_list[0]["children"]
    lyrics_blocks: List[genius.LyricsBlock] = []
    lyrics: List[dict] = []

    # first flatten all the p-s
    lyrics_list = _flatten_lyrics(lyrics_list)
    lyrics_list = list(filter(lambda item: item != "", lyrics_list))

    last_was_br_or_ad: bool = False

    for ly in lyrics_list:
        if ly == {"tag": "br"} or (
            ly["tag"] == "dfp-unit" if isinstance(ly, dict) else False
        ):
            if not last_was_br_or_ad:
                last_was_br_or_ad = True
                lyrics.append(ly)
                continue
            lyrics_blocks.append(
                genius.LyricsBlock.from_api_response(
                    json.dumps(filter_lyrics_list(lyrics))
                )
            )

            lyrics = []
        if isinstance(ly, dict):
            if ly.get("tag", "").lower() in ["h1", "h2", "h3", "h4"]:
                lyrics_blocks.append(
                    genius.LyricsBlock.from_api_response(
                        json.dumps(
                            filter_lyrics_list(lyrics)
                        )
                    )
                )
                lyrics = []
        lyrics.append(ly)
        last_was_br_or_ad = False
    lyrics_blocks.append(
        genius.LyricsBlock.from_api_response(
            json.dumps(filter_lyrics_list(lyrics))
        )
    )
    return lyrics_blocks


def filter_lyrics_list(lyrics_list: list) -> list:
    lyrics_list = map(
        lambda item: "\n"
        if item == {"tag": "br"}
           or (item["tag"] == "dfp-unit" if isinstance(item, dict) else False)
        else item,
        lyrics_list,
    )
    return list(lyrics_list)


def extract_text(lyrics_holder: dict) -> str:
    def extract_one_text(text_holder: dict) -> str:
        if text_holder["tag"] in ["br", "img"]:
            return "\n"
        if text_holder["tag"] in ["p", "a", "i", "b"]:
            return extract_text(text_holder)
        return " "

    return "".join(
        map(
            lambda item: extract_one_text(item)
            if isinstance(item, dict)
            else item,
            lyrics_holder["children"] if "children" in lyrics_holder else {},
        )
    )


def extract_title_from_url(url: str) -> str:
    return url.split("/")[-1].replace("lyrics", "").replace("-", " ").strip()


def get_lookup_url(base_url: str) -> str:
    return f"https://api.genius.com/lookup?url={base_url}"


def get_album_tracks_url(album_id: int) -> str:
    return f"https://api.genius.com/albums/{album_id}/tracks"


def get_album_tracks(album_id: int) -> List:
    return [
        genius.Lyrics.from_api_response(json.dumps(x))
        for x in json.loads(
            get_request_sync(get_album_tracks_url(album_id), build_header())
        )["response"]["tracks"]
    ]


async def get_album_tracks_async(album_id: int) -> List:
    return [
        genius.Lyrics.from_api_response(json.dumps(x))
        for x in json.loads(
            await get_request_async(
                get_album_tracks_url(album_id), build_header()
            )
        )["response"]["tracks"]
    ]
