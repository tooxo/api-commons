from api_commons.common.utils import has_aiohttp
from api_commons.common.web import get_request_sync, get_request_async
from .utils import (
    extract_scripts_from_main_page,
    extract_token_from_script,
)


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
