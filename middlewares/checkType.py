from aiogram.types import Message
from aiogram import BaseMiddleware
from typing import Any, Callable, Dict, Awaitable


class CheckChatTypeMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.chat.type != 'private':
            return
        else:
            return await handler(event, data)
