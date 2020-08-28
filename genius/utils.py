import base64

# this genius key was extracted out of the android app via a mitm attack where
# it was sent with every request as a authorization header

# this key is also different from "normal" genius api keys, because the server
# responds with not only the song meta data but also the lyrics and annotations
import json
from typing import List, Union
from urllib.parse import quote

import genius
from common.web import get_request_sync, get_request_async

GENIUS_SECRET_ENC: str = "VjJ4U2JHRnRPVlZZTWpseFZEQldhR013YkhKV1JHeFlZMnN4UTJGRlNsSlVNMjh5V2xac1RGTjZWbEpXVlhoRVZGVldSR0pWT1c5a2JtUjRZV3hLWVU1c1pHbGpSMFowVW0xVmVsb3lWa2xpYmxwM1RYYzlQUT09"

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


def parse_lyrics(lyrics_catalogue: dict) -> List["genius.LyricsBlock"]:
    lyrics_list: List[Union[str, dict]] = lyrics_catalogue["dom"]["children"][
        0
    ]["children"]
    lyrics_list = list(filter(lambda item: item != "", lyrics_list))
    lyrics_blocks: List[genius.LyricsBlock] = []
    lyrics: List[dict] = []
    cnt: bool = False
    for ly in lyrics_list:
        if ly == {"tag": "br"} or (
            ly["tag"] == "dfp-unit" if isinstance(ly, dict) else False
        ):
            if not cnt:
                cnt = True
                continue
            lyrics_blocks.append(
                genius.LyricsBlock.from_api_response(
                    json.dumps(filter_lyrics_list(lyrics))
                )
            )
            lyrics = []
        lyrics.append(ly)
        cnt = False
    lyrics_blocks.append(
        genius.LyricsBlock.from_api_response(
            json.dumps(filter_lyrics_list(lyrics))
        )
    )
    return lyrics_blocks


def filter_lyrics_list(lyrics_list: list) -> list:
    lyrics_list = filter(lambda item: item != {"tag": "br"}, lyrics_list)
    lyrics_list = filter(
        lambda item: item["tag"] != "dfp-unit"
        if not isinstance(item, str)
        else True,
        lyrics_list,
    )
    return list(lyrics_list)


def extract_text(lyrics_holder: dict) -> str:
    def extract_one_text(text_holder: dict) -> str:
        if text_holder["tag"] in ["br", "img"]:
            return "\n"
        if text_holder["tag"] in ["p", "a", "i"]:
            return extract_text(text_holder)
        return " "

    return "".join(
        map(
            lambda item: extract_one_text(item)
            if isinstance(item, dict)
            else item,
            lyrics_holder["children"],
        )
    )


def extract_title_from_url(url: str) -> str:
    return url.split("/")[-1].replace("lyrics", "").replace("-", " ").strip()
