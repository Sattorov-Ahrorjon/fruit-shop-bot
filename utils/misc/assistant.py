import requests
from typing import Union


class DatabaseRequest:
    def __init__(self, url: str, notify_channel_id: Union[int, str], notify_bot_token: str, redis):
        self.url = url
        self.redis = redis
        self.channel_id = notify_channel_id
        self.bot_token = notify_bot_token

    async def request_sub_error(self, status_code: int, line: int, filename: str, request_type: str = 'POST') -> None:
        message = ("MBG-Store-Bot:\n\n"
                   f"Request {request_type} so'rovda xatolik yuz berdi.\n"
                   f"{filename}  {line}-qator\n"
                   f"requests.status_code: {status_code}")

        requests.post(
            url=f'https://api.telegram.org/bot{self.bot_token}/sendMessage',
            data={'chat_id': self.channel_id, 'text': message}
        )
