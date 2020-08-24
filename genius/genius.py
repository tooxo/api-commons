from common.web import get_request_sync, get_request_async
from genius.search import build_search_url, prepare_search_results

HEADERS = {
    "Host": "genius.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}


class GeniusApi:
    @staticmethod
    def search_genius(search_term: str):
        return prepare_search_results(
            get_request_sync(
                build_search_url(search_term=search_term), extra_headers=HEADERS
            )
        )


class GeniusApiAsync(GeniusApi):
    @staticmethod
    async def search_genius(search_term: str):
        return prepare_search_results(
            await get_request_async(
                build_search_url(search_term=search_term), extra_headers=HEADERS
            )
        )
