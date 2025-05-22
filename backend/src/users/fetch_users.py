import aiohttp
from src.users.schemas import ExternalResponse
from src.config import settings


API_URL = settings.API_URL


async def fetch_users(amount: int) -> ExternalResponse:
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(API_URL, params={"results": amount}) as response:
            data = await response.json()
            return ExternalResponse(**data)