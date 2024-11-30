from aiogram.types import Message
from aiogram import BaseMiddleware
from typing import Any, Callable, Dict, Awaitable


class CheckSubMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        chat_member = await event.bot.get_chat_member(chat_id='Channel_id or Channel_url', user_id=event.from_user.id)

        if chat_member.status == 'left':
            await event.answer(
                text="You are not mourning the channel",
                # reply_markup="channel url in button"
            )
        else:
            return await handler(event, data)
