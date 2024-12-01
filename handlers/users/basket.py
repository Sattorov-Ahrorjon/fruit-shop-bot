from aiogram import Router
from aiogram.types import Message, URLInputFile, CallbackQuery
from utils.misc.redis_service import RedisService
from utils.db_api.views import user_detail, product_detail
from keyboards.default.product import (
    basket_product_keyboard as b_p_keyboard,
    basket_product
)
from keyboards.inline.product import delete_or_pay_product

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


def product_caption(product, lang, order_num):
    name = product.get('name')
    price = product.get('price')
    amount = Amount.get(lang).get(product.get('amount'))
    caption = {
        'uz': (f"Mahsulot nomi {name}\n"
               f"Ushbu mahsulotning {amount} {price} so'm.\n"
               f"🧺 Sizning savatingizda {order_num} {amount} bor\n"
               f"🧮 Jami narxi {int(order_num) * int(price)} so'm"),
        'ru': (f"Название продукта {name}\n"
               f"{amount} этого продукта {price} сум.\n"
               f"🧺 У вас в корзине {order_num} {amount}\n"
               f"🧮 Общая стоимость {int(order_num) * int(price)} сум")
    }
    return caption.get(lang)


@router.message(lambda msg: msg.text in ("Моя корзина 🧺", "Meni savatim 🧺"))
async def user_basket(message: Message):
    # _redis.flush_all()
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    answer_text = {
        'uz': "Sizding savatingizdagi mahsulotlar. 🍎🍇\n"
              "Batafsil ko'rish uchun mahsulot nomini tanlang.",
        'ru': "Товары в вашей корзине. 🍎🍇\n"
              "Выберите название продукта, чтобы просмотреть подробности."
    }.get(user_lang)
    await message.answer(
        text=answer_text,
        reply_markup=b_p_keyboard(pk=message.from_user.id, lang=user_lang)
    )


@router.message(lambda msg: msg.text in basket_product(msg.from_user.id))
async def user_basket_detail(message: Message):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    p_name = message.text.split('🧺')[0].strip()
    product_pk = _redis.get_product_pk(lang=user_lang, p_name=p_name)
    result = await product_detail(pk=product_pk, lang=user_lang)
    product = result.get('result')
    order_number = _redis.get_user_basket(message.from_user.id).get(p_name)
    caption = product_caption(product=product, lang=user_lang, order_num=order_number)
    await message.answer_photo(
        photo=URLInputFile(product.get('image')),
        caption=caption,
        reply_markup=delete_or_pay_product(lang=user_lang, product_name=p_name)
    )


@router.callback_query(lambda call: call.data.startswith('basket_'))
async def clear_basket(call: CallbackQuery):
    await call.message.delete()
    result = await user_detail(call.from_user.id)
    user_lang = result.get('result').get('language')
    product_name = call.data.split('basket_')[1]
    _redis.delete_user_basket(pk=call.from_user.id, product_name=product_name)
    answer_text = {
        'uz': "Mahsulot savatdan o'chirildi ❌\n\n"
              "Sizding savatingizdagi mahsulotlar. 🍎🍇\n"
              "Batafsil ko'rish uchun mahsulot nomini tanlang.",
        'ru': "Товар удален из корзины ❌\n\n"
              "Товары в вашей корзине. 🍎🍇\n"
              "Выберите название продукта, чтобы просмотреть подробности."
    }.get(user_lang)
    await call.message.answer(
        text=answer_text,
        reply_markup=b_p_keyboard(pk=call.from_user.id, lang=user_lang)
    )
