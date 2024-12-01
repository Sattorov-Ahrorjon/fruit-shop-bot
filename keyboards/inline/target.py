from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def target_check():
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="target_send")
            ],
            [
                InlineKeyboardButton(text="Bekor qilish ❌", callback_data="target_cancel")
            ]
        ]
    )
    return btn
