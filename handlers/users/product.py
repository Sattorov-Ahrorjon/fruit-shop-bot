from aiogram import Router
from aiogram.types import Message, URLInputFile
from aiogram.fsm.context import FSMContext
from utils.db_api.views import product_detail, user_detail
from utils.misc.redis_service import RedisService
from keyboards.default.product import (
    product_number_keyboard, products_keyboard
)

router = Router()

_redis = RedisService()

Amount = {
    'uz': {
        1: "dona",
        2: "kg"
    },
    'ru': {
        1: "шт",
        2: "кг"
    }
}


def product_caption(product, lang):
    name = product.get('name')
    price = product.get('price')
    amount = Amount.get(lang).get(product.get('amount'))
    about = product.get('description')
    caption = {
        'uz': (f"<b>Nomi:</b> {name}\n\n"
               f"<b>Haqida:</b>{about}\n\n"
               f"<b>Narxi:</b> {price} so'm/{amount}.\n"),
        'ru': (f"<b>Имя:</b> {name}\n\n"
               f"<b>О продукте:</b> {about}\n\n"
               f"<b>Стоимость:</b> {price} сум/{amount}.\n"),
    }
    return caption.get(lang)


@router.message(lambda msg: msg.text in _redis.get_all_products())
async def product_detail_handler(message: Message, state: FSMContext):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    product_pk = _redis.get_product_pk(p_name=message.text)
    result = await product_detail(pk=product_pk, lang=user_lang)
    product = result.get('result')
    caption = product_caption(product, user_lang)
    await message.answer_photo(
        photo=URLInputFile(url=product.get('image')),
        caption=caption,
        reply_markup=product_number_keyboard(user_lang)
    )
    await state.update_data(data={'product_name': message.text})


@router.message(lambda msg: msg.text is not None and msg.text.isdigit())
async def product_number_handler(message: Message, state: FSMContext):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    data = await state.get_data()
    product_name = data.get('product_name')
    number = str(int(message.text))
    _redis.set_user_basket(
        pk=message.from_user.id,
        data={f'{product_name}': number}
    )
    answer_text = {
        'uz': "✅ Mahsulot savatga qo'shildi 🧺\n\n"
              "Yana boshqa mahsulotni tanlaymizmi 🙂",
        'ru': "✅ Товар добавлен в корзину 🧺\n\n"
              "Выберем другой продукт 🙂"
    }
    await message.answer(
        text=answer_text.get(user_lang),
        reply_markup=await products_keyboard(user_lang)
    )
    await state.clear()
