import json
from dataclasses import dataclass
from urllib.parse import quote

from typing import List

from api_commons import genius
from api_commons.common.error import NoResultsFound

BASE_URL = "https://genius.com/api/search/song?q={}"


def build_search_url(search_term: str) -> str:
    return BASE_URL.format(quote(search_term))


def prepare_search_results(raw_response: str) -> List["genius.SearchResult"]:
    raw_response = raw_response
    parsed: dict = json.loads(raw_response)
    hits: List[dict] = parsed["response"]["sections"][0]["hits"]
    if not hits:
        raise NoResultsFound("No results found.")
    return sorted(
        [
            genius.SearchResult.from_api_response(json.dumps(x["result"]))
            for x in hits
        ],
        key=lambda i: i.stats.pageviews or 0,
        reverse=True,
    )


@dataclass
class SearchResult:
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
    primary_artist: "genius.Artist"

    def to_lyrics(self, load_annotations: bool = True) -> "genius.Lyrics":
        lyrics: genius.Lyrics = genius.Lyrics.get_by_id(song_id=str(self.id))
        if load_annotations:
            lyrics.load_annotations()
        return lyrics

    async def to_lyrics_async(
        self, load_annotations: bool = True
    ) -> "genius.Lyrics":
        lyrics: genius.Lyrics = await genius.Lyrics.get_by_id_async(
            song_id=str(self.id)
        )
        if load_annotations:
            await lyrics.load_annotations_async()
        return lyrics

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)

        parsed_api_response["stats"] = genius.Stats.from_api_response(
            json.dumps(parsed_api_response["stats"])
        )
        parsed_api_response["primary_artist"] = genius.Artist.from_api_response(
            json.dumps(parsed_api_response["primary_artist"])
        )
        return cls(
            **{
                k: v
                for k, v in parsed_api_response.items()
                if k in cls.__annotations__.keys()
            }
        )
