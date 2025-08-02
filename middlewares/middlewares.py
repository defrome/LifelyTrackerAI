from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        async for session in get_db():
            data["session"] = session
            return await handler(event, data)