from api_commons.common.utils import has_aiohttp
from api_commons.common.web import get_request_sync, get_request_async
from .utils import (
    extract_scripts_from_main_page,
    extract_token_from_script, COMMON_HEADERS,
)
from .search import SearchTypes, build_search_url, parse_search_result_track, \
    parse_search_result_artist, parse_search_result_album


class SoundCloudApi:
    def __init__(self):
        self.api_token = None

    def get_api_token(self) -> str:
        if self.api_token:
            return self.api_token
        for script in extract_scripts_from_main_page(
            get_request_sync("https://soundcloud.com")
        ):
            script_src = get_request_sync(script)
            api_token = extract_token_from_script(script_src)
            if not api_token:
                continue
            self.api_token = api_token
            return self.api_token

    def search(self, search_term: str, search_type: SearchTypes,
               search_results=30):
        url = build_search_url(
            search_term=search_term, search_type=search_type,
            client_id=self.get_api_token(),
            search_results=search_results
        )
        api_response: str = get_request_sync(
            url=url, extra_headers=COMMON_HEADERS
        )
        if search_type in [SearchTypes.GO_TRACK, SearchTypes.TRACK]:
            return parse_search_result_track(
                api_response
            )
        if search_type == SearchTypes.ARTIST:
            return parse_search_result_artist(
                api_response
            )
        if search_type == SearchTypes.ALBUM:
            return parse_search_result_album(api_response)
        if search_type == SearchTypes.ALL:
            try:
                return parse_search_result_track(
                    api_response
                )
            except:
                try:
                    return parse_search_result_artist(
                        api_response
                    )
                except:
                    try:
                        return parse_search_result_album(
                            api_response
                        )
                    except:
                        pass
        return None


class SoundCloudApiAsync(SoundCloudApi):
    @has_aiohttp
    async def get_api_token(self) -> str:
        if self.api_token:
            return self.api_token
        for script in extract_scripts_from_main_page(
            await get_request_async("https://soundcloud.com")
        ):
            script_src = await get_request_async(script)
            api_token = extract_token_from_script(script_src)
            if not api_token:
                continue
            self.api_token = api_token
            return self.api_token

    @has_aiohttp
    async def search(self, search_term: str, search_type: SearchTypes):
        url = build_search_url(
            search_term=search_term, search_type=search_type,
            client_id=await self.get_api_token()
        )
        api_response: str = await get_request_async(
            url=url, extra_headers=COMMON_HEADERS
        )
        if search_type in [SearchTypes.GO_TRACK, SearchTypes.TRACK]:
            return parse_search_result_track(
                api_response
            )
        if search_type == SearchTypes.ARTIST:
            return parse_search_result_track(
                api_response
            )
        return None
