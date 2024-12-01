import aiohttp
from aiogram.types import Message
from data.config import BACKEND_URL as domain
from data.config import GROUP_ID, BOT_TOKEN as bot_token, ADMINS


async def group_notify(message: str = ''):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=f'https://api.telegram.org/bot{bot_token}/sendMessage',
                data={'chat_id': GROUP_ID, 'text': message}
        ) as resp:
            response = await resp.json()
            return response


async def group_notify_map(message: Message, data: dict):
    await message.bot.send_location(
        chat_id=GROUP_ID,
        latitude=data.get('lat'),
        longitude=data.get('lon')
    )


async def user_create(data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{domain}/user/', data=data) as resp:
            if resp.status == 201:
                result = await resp.json()
                return result
            return


async def user_detail(pk):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{domain}/user/{pk}/') as resp:
            if resp.status == 200:
                response = await resp.json()
                return response
            return {}


async def user_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{domain}/user/') as resp:
            response = await resp.json()
            return response


async def user_check(pk):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{domain}/user/check/{pk}/") as resp:
            if resp.status == 200:
                return True
            return False


async def product_list(lang):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{domain}/product/', headers={'Accept-Language': lang}) as resp:
            if resp.status == 200:
                response = await resp.json()
                return response
            return {}


async def product_detail(pk, lang):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{domain}/product/{pk}/', headers={'Accept-Language': lang}) as resp:
            if resp.status == 200:
                response = await resp.json()
                return response
            return {}


async def order_create(data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{domain}/order/', data=data) as resp:
            response = await resp.json()
            return response


async def order_detail(pk, name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{domain}/order/{pk}/?order_name={name}') as resp:
            response = await resp.json()
            return response


async def order_list(pk):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{domain}/order/{pk}/') as resp:
            response = await resp.json()
            return response


async def sendAdvertisement(message: Message, msg_id):
    result = await user_list()
    users = result.get('result')
    success = 0
    failed = 0
    async with aiohttp.ClientSession() as session:
        for user in users:
            async with session.post(
                    url=f"https://api.telegram.org/bot{bot_token}/forwardMessage",
                    data={
                        "chat_id": user.get('telegram_id'),
                        "from_chat_id": message.chat.id,
                        "message_id": msg_id,
                    }) as resp:
                if resp.status == 200:
                    success += 1
                if resp.status != 200:
                    failed += 1
    return success, failed
