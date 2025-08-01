import aiohttp
import async_timeout

from conf import settings


async def make_request(
    url: str,
    method: str,
    data: dict = None,
    headers: dict = None
):
    if not data:
        data = {}

    async with async_timeout.timeout(settings.GATEWAY_TIMEOUT):
        async with aiohttp.ClientSession() as session:
            request = getattr(session, method)
            async with request(url, json=data, headers=headers) as response:
                data = await response.json()
                return (data, response.status)