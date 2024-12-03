# from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


# def delete_or_pay_product(lang, product_name):
#     delete_text = {
#         'uz': "Savatdan o'chirish ❌",
#         'ru': "Удалить из корзины ❌"
#     }.get(lang)
#     pay_text = {
#         'uz': "Mahsulot uchun to'lash 💸",
#         'ru': "Оплата за продукт 💸"
#     }.get(lang)
#     brn = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text=pay_text, callback_data=f"pay_{product_name}")
#             ],
#             [
#                 InlineKeyboardButton(text=delete_text, callback_data=f"basket_{product_name}")
#             ]
#         ]
#     )
#     return brn
