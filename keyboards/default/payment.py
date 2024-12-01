from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from .product import Text

PayTypes = {
    'uz': ['Click 📱', 'Payme 📱', 'Terminal 💳', 'Naqt pul 💸'],
    'ru': ['Click 📱', 'Payme 📱', 'Терминал 💳', 'Наличные деньги 💸']
}


def payment_list():
    return PayTypes['uz'] + PayTypes['ru']


def pay_type_keyboard(lang):
    btn = ReplyKeyboardBuilder()
    pay_types = PayTypes.get(lang)
    for pay in pay_types:
        btn.add(KeyboardButton(text=pay))
    btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    btn.adjust(*[2])
    return btn.as_markup(resize_keyboard=True)


def driver_time_keyboard(lang):
    btn = ReplyKeyboardBuilder()
    btn.add(KeyboardButton(text=Text.get('mainBtn').get(lang)))
    btn.add(KeyboardButton(text=Text.get('driverTimeBtn').get(lang)))
    btn.adjust(*[2])
    return btn.as_markup(resize_keyboard=True)


def location_keyboard(lang):
    btn = ReplyKeyboardBuilder()
    btn.add(KeyboardButton(text=Text.get('locationBtn').get(lang), request_location=True))
    btn.adjust(*[1])
    return btn.as_markup(resize_keyboard=True)
