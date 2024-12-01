from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from utils.misc.redis_service import RedisService
from states.payment import PaymentState
from utils.regex_phone import regex_phone
from keyboards.default.product import products_keyboard
from utils.db_api.views import (
    user_detail, user_create, order_create,
    group_notify)
from keyboards.default.payment import (
    pay_type_keyboard, payment_list, driver_time_keyboard,
    location_keyboard
)

router = Router()

_redis = RedisService()
PayText = {
    'uz': "Sizga qanday usulda to'lov qilish qulay ?\n"
          "Berilgan to'lov turlaridan birini tanlang",
    'ru': "Каким способом вам удобно производить оплату ?\n"
          "Выберите один из предоставленных видов оплаты"
}

TimeText = {
    'uz': "Yetkazib berish vaqtini yuboring 🚚\n"
          "Masalan 1 aprel 14.00 da 🕑.",
    'ru': "Сообщите время доставки 🚚\n"
          "Например, 1 апреля в 14:00 🕑."
}

LocationText = {
    'uz': "Mahsulotni yetkazib berishimiz uchun joylashuv "
          "malumotingizni berilgan tugma 👇 orqali yoki yozma ravishda yuboring",
    'ru': "Пожалуйста, отправьте нам информацию о своем местонахождении с помощью "
          "предоставленной кнопки 👇 или в письменном виде, чтобы мы могли доставить продукт."
}

PhoneText = {
    'uz': "Siz bilan bog'lanishimiz uchun qo'shimcha telefon raqam kiriting.\n"
          "Iltimos berilgan shaklda yuboring +998902223344",
    'ru': "Введите дополнительный номер телефона, чтобы мы могли связаться с вами.\n"
          "Отправьте пожалуйста по данной форме +998902223344"
}

DoneText = {
    'uz': "Malumotlar muvaffaqiyatli saqlandi ✅",
    'ru': "Данные успешно сохранены ✅"
}


@router.message(lambda msg: msg.text in ("Barchasiga to'lash 💸", "Платить за все 💸"))
async def all_to_pay(message: Message, state: FSMContext):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    user_basket = _redis.get_user_basket(message.from_user.id)
    if not user_basket:
        await message.answer(
            text={
                'uz': "Sizning savatingiz bo'sh 😕",
                'ru': "Ваша корзина пуста 😕"
            }.get(user_lang)
        )
        return
    answer_text = PayText.get(user_lang)
    await message.answer(
        text=answer_text,
        reply_markup=pay_type_keyboard(user_lang)
    )
    await state.update_data(data={'product': 'all'})
    await state.set_state(PaymentState.pay_type)


@router.callback_query(lambda call: call.data.startswith("pay_"))
async def product_to_pay(call: CallbackQuery, state: FSMContext):
    result = await user_detail(call.message.from_user.id)
    user_lang = result.get('result').get('language')
    answer_text = PayText.get(user_lang)
    await call.message.answer(
        text=answer_text,
        reply_markup=pay_type_keyboard(user_lang)
    )
    await state.update_data(data={'product': call.data.split('pay_')[1]})
    await state.set_state(PaymentState.pay_type)


@router.message(PaymentState.pay_type, lambda msg: msg.text in payment_list())
async def uz_to_pay(message: Message, state: FSMContext):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    answer_text = TimeText.get(user_lang)
    await message.answer(
        text=answer_text,
        reply_markup=driver_time_keyboard(lang=user_lang)
    )
    await state.update_data(data={'pay_type': message.text})
    await state.set_state(PaymentState.deliver_time)


@router.message(PaymentState.pay_type, lambda msg: msg.text not in payment_list())
async def uz_to_pay(message: Message):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    await message.answer(
        text={
            'uz': "Iltimos berilgan to'lov turlaridan birini tanlang 👇",
            'ru': "Пожалуйста, выберите один из указанных типов оплаты 👇"
        }.get(user_lang)
    )


@router.message(PaymentState.deliver_time)
async def transferred_to_location(message: Message, state: FSMContext):
    if message.text not in ("O'tqazib yuborish. ➡", "Пропуск. ➡"):
        await state.update_data(data={'deliver_time': message.text})
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    answer_text = LocationText.get(user_lang)
    await message.answer(
        text=answer_text,
        reply_markup=location_keyboard(user_lang)
    )
    await state.set_state(PaymentState.location)


@router.message(PaymentState.location, lambda msg: msg.location is not None)
async def location_create(message: Message, state: FSMContext):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    answer_text = PhoneText.get(user_lang)
    await message.answer(
        text=answer_text,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(
        data={'location': {
            'lat': message.location.latitude, 'lon': message.location.longitude}
        }
    )
    await state.set_state(PaymentState.phone)


@router.message(PaymentState.location, lambda msg: msg.location is None)
async def location_create(message: Message):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    await message.answer(
        text={
            'uz': "Iltimos berilgan tugma orqali joylashuv malumotingizni yuboring 👇.",
            'ru': "Пожалуйста, отправьте информацию о своем местоположении, используя соответствующую кнопку 👇."
        }.get(user_lang),
        reply_markup=location_keyboard(user_lang)
    )


@router.message(PaymentState.phone, lambda msg: msg.text and regex_phone(msg.text))
async def create_phone(message: Message, state: FSMContext):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    answer_text = DoneText.get(user_lang)
    await message.answer(
        text=answer_text,
        reply_markup=await products_keyboard(user_lang)
    )
    await state.update_data(data={'phone': message.text})
    data = await state.get_data()
    products = _redis.get_user_basket(message.from_user.id)
    if data.get('product') != 'all':
        amount = products.get(data.get('product'))
        products = {data.get('product'): amount}

    # product_pk = _redis.get_product_pk(lang=user_lang, p_name=)

    await order_create(
        data={
            "name": "string",
            "price": 9223372036854776000,
            "total_price": 9223372036854776000,
            "count": 9223372036854776000
        }
    )

    _redis.delete_user_basket(pk=message.from_user.id, _all=True)
    await state.clear()


@router.message(PaymentState.phone, lambda msg: msg.text and not regex_phone(msg.text))
async def create_phone(message: Message):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    await message.answer(
        text={
            'uz': "Iltimos ko'rsatilgan tartibda (+998902223344) telefon raqam yuboring!",
            'ru': "Пожалуйста, пришлите номер телефона в указанном порядке (+998902223344)!"
        }.get(user_lang)
    )
