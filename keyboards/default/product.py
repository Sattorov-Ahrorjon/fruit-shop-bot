from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from utils.db_api.views import product_list

Text = {
    'mainBtn': {
        'uz': "Bosh sahifa 🏠",
        'ru': "Главная 🏠"
    }
}


async def products_keyboard(lang):
    btn = ReplyKeyboardBuilder()
    result = await product_list(lang)
    # if not result:
    #     btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    #     return btn.as_markup(resize_keyboard=True)
    products = result.get('result')
    for prd in products:
        btn.add(KeyboardButton(text=f"{prd.get('name')} {prd.get('price')} so'm"))
    btn.adjust(*[3])
    btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    return btn.as_markup(resize_keyboard=True)
