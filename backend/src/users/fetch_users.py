import aiohttp
import asyncio

from pydantic import ValidationError
from src.users.schemas import ExternalResponse
from src.config import settings


API_URL = settings.API_URL


async def fetch_users(amount: int) -> ExternalResponse:
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(API_URL, params={"results": amount}) as response:
                data = await response.json()
                return ExternalResponse(**data)
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"Ошибка при запросе к внешнему API: {e}")
    except ValidationError as e:
        print(f"Ошибка валидации данных от API: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")

    return None