from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from utils.db_api.views import product_list
from utils.misc.redis_service import RedisService

_redis = RedisService()

Text = {
    'mainBtn': {
        'uz': "Bosh sahifa 🏠",
        'ru': "Главная 🏠"
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

ProductNumber = {
    '1️⃣': '1', '2️⃣': '2', '3️⃣': '3',
    '4️⃣': '4', '5️⃣': '5', '6️⃣': '6',
    '7️⃣': '7', '8️⃣': '8', '9️⃣': '9',
    '🔟': '10'
}


async def create_products_price(products):
    result = {}
    for pr in products:
        result.update({f"{pr.get('name')} {pr.get('price')} so'm": str(pr.get('price'))})
    _redis.set_products_price(result)


def product_dict(data):
    result = {}
    for pr in data:
        result.update({f"{pr.get('name')} {pr.get('price')} so'm": str(pr.get('id'))})
    return result


async def products_keyboard(lang):
    btn = ReplyKeyboardBuilder()
    result = await product_list(lang)
    products = product_dict(result.get('result'))
    _redis.set_products(lang=lang, products=products)
    await create_products_price(products)
    for prd in products:
        btn.add(KeyboardButton(text=prd))
    btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    btn.add(KeyboardButton(text=Text.get('basketBtn').get(lang)))

    key_order = []
    len(products) == 1 and key_order.append(1)
    len(products) >= 2 and key_order.append(2)
    len(products) > 2 and len(products) % 2 == 1 and key_order.append(1)
    key_order.append(2)
    btn.adjust(*key_order)
    return btn.as_markup(resize_keyboard=True)


def product_number_keyboard(lang):
    btn = ReplyKeyboardBuilder()
    for text in ProductNumber:
        btn.add(KeyboardButton(text=text))
    btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    btn.adjust(*[3, 3, 3, 1, 2])
    return btn.as_markup(resize_keyboard=True)


def basket_product(pk):
    products = _redis.get_user_basket(pk)
    return list(map(lambda text: text + ' ' + '🧺', products))


def basket_product_keyboard(pk, lang):
    products = basket_product(pk)
    btn = ReplyKeyboardBuilder()
    for name in products:
        btn.add(KeyboardButton(text=name))
    btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    btn.add(KeyboardButton(text=Text.get('payBtn').get(lang)))
    prod = []
    len(products) >= 2 and prod.append(2)
    len(products) == 1 and prod.append(1)
    len(products) > 2 and len(products) % 2 == 1 and prod.append(1)
    prod.append(2)
    btn.adjust(*prod)
    return btn.as_markup(resize_keyboard=True)
