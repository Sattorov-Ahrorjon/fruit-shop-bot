from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def language():
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="O'zbek tili 🇺🇿"),
                KeyboardButton(text="Русский язык 🇷🇺")
            ]
        ],
        resize_keyboard=True
    )
    return btn


def phone_number_btn():
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Telefon raqam 📱", request_contact=True)
            ]
        ],
        resize_keyboard=True
    )
    return btn
