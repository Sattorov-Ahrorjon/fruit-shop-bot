import aiohttp
from data.config import BACKEND_URL as domain


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
            response = await resp.json()
            return response


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
            return


async def product_detail(pk):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{domain}/product/{pk}/') as resp:
            response = await resp.json()
            return response


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
