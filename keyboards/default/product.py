from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from utils.db_api.views import product_list
from utils.misc.redis_service import RedisService

_redis = RedisService()

Text = {
    'mainBtn': {
        'uz': "Bosh sahifa 🏠",
        'ru': "Главная 🏠"
    },
    'langBtn': {
        'uz': "Til ♻️",
        'ru': "Язык ♻️"
    },
    'basketBtn': {
        'uz': "Meni savatim 🧺",
        'ru': "Моя корзина 🧺"
    },
    'payBtn': {
        'uz': "Barchasiga to'lash 💸",
        'ru': "Платить за все 💸"
    },
    'driverTimeBtn': {
        'uz': "O'tqazib yuborish. ➡",
        'ru': "Пропуск. ➡"
    },
    'locationBtn': {
        'uz': "Joylashuvni yuborish 🚩",
        'ru': "Отправить местоположение 🚩"
    }
}


async def create_products_price(products, lang):
    result = {}
    unit = {'uz': "so'm", 'ru': 'сум'}.get(lang)
    for pr in products:
        result.update({f"{pr.get('name')} {pr.get('price')} {unit}": str(pr.get('price'))})
    _redis.set_products_price(result)


def product_dict(data, lang):
    result = {}
    unit = {'uz': "so'm", 'ru': 'сум'}.get(lang)
    for pr in data:
        result.update({f"{pr.get('name')} {pr.get('price')} {unit}": str(pr.get('id'))})
    return result


async def products_keyboard(lang):
    btn = ReplyKeyboardBuilder()
    result = await product_list(lang)
    if not result.get('result'):
        btn.add(KeyboardButton(text=Text.get('langBtn').get(lang)))
        btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
        btn.add(KeyboardButton(text=Text.get('basketBtn').get(lang)))
        btn.adjust(*[3])
        return btn.as_markup(resize_keyboard=True)
    await create_products_price(result.get('result'), lang)
    products = product_dict(result.get('result'), lang)
    _redis.set_products(products=products)
    for prd in products:
        btn.add(KeyboardButton(text=prd))
    btn.add(KeyboardButton(text=Text.get('langBtn').get(lang)))
    btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    btn.add(KeyboardButton(text=Text.get('basketBtn').get(lang)))

    key_order = []
    for i in range(len(products)):
        key_order.append(1)
    key_order.append(3)
    btn.adjust(*key_order)
    return btn.as_markup(resize_keyboard=True)


def product_number_keyboard(lang):
    btn = ReplyKeyboardBuilder()
    for text in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
        btn.add(KeyboardButton(text=text))
    btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    btn.adjust(*[3, 3, 3, 1, 2])
    return btn.as_markup(resize_keyboard=True)


def basket_product(pk):
    products = _redis.get_user_basket(pk)
    return list(map(lambda text: text + ' ' + '❌', products))


def basket_product_keyboard(pk, lang):
    products = basket_product(pk)
    btn = ReplyKeyboardBuilder()
    if not products:
        return
    for name in products:
        btn.add(KeyboardButton(text=name))
    btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    btn.add(KeyboardButton(text=Text.get('payBtn').get(lang)))
    prod = []
    for i in range(len(products)):
        prod.append(1)
    prod.append(2)
    btn.adjust(*prod)
    return btn.as_markup(resize_keyboard=True)
