import json
from urllib.parse import quote
import api_commons.soundcloud


class SearchTypes:
    TRACK = "/tracks"
    GO_TRACK = "go_tracks"
    ARTIST = "/users"
    ALBUM = "/albums"
    ALL = ""


def build_search_url(search_term: str, client_id: str,
                     search_type: SearchTypes, search_results=30):
    return (
        f"https://api-v2.soundcloud.com/search"
        f"{search_type if search_type != SearchTypes.GO_TRACK else '/tracks'}?q="
        f"{quote(search_term)}&client_id={client_id}"
        f"{'&filter.content_tier=SUB_HIGH_TIER' if search_type == SearchTypes.GO_TRACK else ''}&limit={search_results}"
    )


def parse_search_result_track(raw_json_response: str):
    parsed_response = json.loads(raw_json_response)
    return [
        api_commons.soundcloud.Track.from_api_response(
            json.dumps(x)
        ) for x in parsed_response["collection"]
    ]


def parse_search_result_artist(raw_json_response: str):
    parsed_response = json.loads(raw_json_response)
    return [
        api_commons.soundcloud.User.from_api_response(
            json.dumps(x)
        ) for x in parsed_response["collection"]
    ]


def parse_search_result_album(raw_json_response: str):
    parsed_response = json.loads(raw_json_response)
    return [
        api_commons.soundcloud.Album.from_api_response(
            json.dumps(x)
        ) for x in parsed_response["collection"]
    ]
