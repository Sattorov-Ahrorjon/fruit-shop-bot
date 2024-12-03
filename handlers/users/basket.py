from aiogram import Router
from aiogram.types import Message, CallbackQuery  # URLInputFile
from utils.misc.redis_service import RedisService
from utils.db_api.views import user_detail
from keyboards.default.product import (
    basket_product_keyboard as b_p_keyboard,
    basket_product, products_keyboard
)

router = Router()

_redis = RedisService()

Amount = {
    'uz': {
        1: "dona",
        2: "kilogram"
    },
    'ru': {
        1: "шт.",
        2: "кг"
    }
}


def user_basket_orders(pk, lang):
    orders = _redis.get_user_basket(pk)
    order_text = ''
    total_price = 0
    for name, number in orders.items():
        price = _redis.get_product_price(name)
        total_price += int(number) * int(price)
        order_text += (f"🔅 {name}\n"
                       f"🧮  {number} x {price} = {int(number) * int(price)}\n\n")

    order_text += f"💲 {total_price}"
    return order_text



@router.message(lambda msg: msg.text in ("Моя корзина 🧺", "Meni savatim 🧺"))
async def user_basket(message: Message):
    # _redis.flush_all()
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    key_btn = b_p_keyboard(pk=message.from_user.id, lang=user_lang)
    if not key_btn:
        await message.answer(
            text={
                'uz': "Savatingiz bo'sh ekan 😕",
                'ru': "Ваша корзина пуста 😕"
            }.get(user_lang)
        )
        return
    await message.answer(
        text={
            'uz': "🧺 mahsulotlar. 🍎🍇\n\n"
                  "Bekor qilish uchun «Mahsulot nomi ❌»\n"
                  "Savatni tozalash uchun «Tozalash 🔄»",
            'ru': "Товары в вашей корзине. 🍎🍇\n\n"
                  "«❌ Название продукта» для отмены\n"
                  "«🔄 Очистить», чтобы очистить корзину."
        }.get(user_lang),
        reply_markup=key_btn
    )
    order_text = user_basket_orders(message.from_user.id, user_lang)
    await message.answer(
        text=order_text
    )


@router.message(lambda msg: msg.text in basket_product(msg.from_user.id))
async def user_basket_delete(message: Message):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    p_name = message.text.split('❌')[0].strip()
    _redis.delete_user_basket(pk=message.from_user.id, product_name=p_name)
    key_btn = b_p_keyboard(pk=message.from_user.id, lang=user_lang)
    if not key_btn:
        await message.answer(
            text={
                'uz': "🏠 Siz asosiy sahifadasiz\n\n"
                      "Kerakli buyuruqni tanlang 👇",
                'ru': "🏠 Вы находитесь на главной странице\n\n"
                      "Выберите нужную команду 👇"
            }.get(user_lang),
            reply_markup=await products_keyboard(user_lang)
        )
        return
    await message.answer(
        text={
            'uz': "🧺 mahsulotlar. 🍎🍇\n\n"
                  "Bekor qilish uchun «Mahsulot nomi ❌»\n"
                  "Savatni tozalash uchun «Tozalash 🔄»",
            'ru': "Товары в вашей корзине. 🍎🍇\n\n"
                  "«❌ Название продукта» для отмены\n"
                  "«🔄 Очистить», чтобы очистить корзину."
        }.get(user_lang),
        reply_markup=key_btn
    )
    order_text = user_basket_orders(message.from_user.id, user_lang)
    await message.answer(
        text=order_text
    )

# @router.message(lambda msg: msg.text in basket_product(msg.from_user.id))
# async def user_basket_detail(message: Message):
#     result = await user_detail(message.from_user.id)
#     user_lang = result.get('result').get('language')
#     p_name = message.text.split('🧺')[0].strip()
#     product_pk = _redis.get_product_pk(lang=user_lang, p_name=p_name)
#     result = await product_detail(pk=product_pk, lang=user_lang)
#     product = result.get('result')
#     order_number = _redis.get_user_basket(message.from_user.id).get(p_name)
#     caption = product_caption(product=product, lang=user_lang, order_num=order_number)
#     await message.answer_photo(
#         photo=URLInputFile(product.get('image')),
#         caption=caption,
#         reply_markup=delete_or_pay_product(lang=user_lang, product_name=p_name)
#     )


# @router.callback_query(lambda call: call.data.startswith('basket_'))
# async def clear_basket(call: CallbackQuery):
#     await call.message.delete()
#     result = await user_detail(call.from_user.id)
#     user_lang = result.get('result').get('language')
#     product_name = call.data.split('basket_')[1]
#     _redis.delete_user_basket(pk=call.from_user.id, product_name=product_name)
#     answer_text = {
#         'uz': "Mahsulot savatdan o'chirildi ❌\n\n"
#               "Sizding savatingizdagi mahsulotlar. 🍎🍇\n"
#               "Batafsil ko'rish uchun mahsulot nomini tanlang.",
#         'ru': "Товар удален из корзины ❌\n\n"
#               "Товары в вашей корзине. 🍎🍇\n"
#               "Выберите название продукта, чтобы просмотреть подробности."
#     }.get(user_lang)
#     await call.message.answer(
#         text=answer_text,
#         reply_markup=b_p_keyboard(pk=call.from_user.id, lang=user_lang)
#     )
