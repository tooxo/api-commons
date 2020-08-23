from urllib.request import urlopen, Request

try:
    import aiohttp
except ModuleNotFoundError:
    pass  # aiohttp not found, async requests not possible


def get_request_sync(url: str, extra_headers=None) -> str:
    if extra_headers is None:
        extra_headers = {}
    req: Request = Request(url=url, headers=extra_headers)
    with urlopen(req) as response:
        return response.read().decode()


async def get_request_async(url: str, extra_headers=None) -> str:
    if extra_headers is None:
        extra_headers = {}
    async with aiohttp.request("GET", url=url, headers=extra_headers) as req:
        return await req.text()


def post_request_sync(url: str, payload: str = None, extra_headers=None) -> str:
    if extra_headers is None:
        extra_headers = {}
    req: Request = Request(
        url=url, data=payload.encode(), headers=extra_headers
    )
    with urlopen(req) as response:
        return response.read().decode()


async def post_request_async(
    url: str, payload: str = None, extra_headers=None
) -> str:
    if extra_headers is None:
        extra_headers = {}
    async with aiohttp.request(
        "POST", url=url, data=payload, headers=extra_headers
    ) as res:
        return await res.text()
