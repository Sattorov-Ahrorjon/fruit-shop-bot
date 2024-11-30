import requests
from aiogram import types
from typing import Union, Optional
from data.config import (
    NOTIFY_BOT_TOKEN,
    NOTIFY_CHANNEL_ID
)


async def request_sub_error(status_code: int, line: int, filename: str, request_type: str = 'POST') -> None:
    message = ("MBG-Store-Bot:\n\n"
               f"Request {request_type} so'rovda xatolik yuz berdi.\n"
               f"{filename}  {line}-qator\n"
               f"requests.status_code: {status_code}")

    requests.post(
        url=f'https://api.telegram.org/bot{NOTIFY_BOT_TOKEN}/sendMessage',
        data={'chat_id': NOTIFY_CHANNEL_ID, 'text': message}
    )


async def network_error_message(
        message: types.Message,
        button: Optional[
            Union[
                types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove
            ]
        ] = None
):
    if button is None:
        await message.answer(
            text="Tarmoqda ulanish xatoligi yuz berdi\n"
                 "Iltimos qaytadan urinib ko'ring.\n\n"
                 "Произошла ошибка подключения к сети\n"
                 "Пожалуйста, попробуйте еще раз."
        )
    else:
        await message.answer(
            text="Tarmoqda ulanish xatoligi yuz berdi\n"
                 "Iltimos qaytadan urinib ko'ring.\n\n"
                 "Произошла ошибка подключения к сети\n"
                 "Пожалуйста, попробуйте еще раз.",
            reply_markup=button
        )
