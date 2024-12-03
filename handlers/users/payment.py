from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from utils.misc.redis_service import RedisService
from states.payment import PaymentState
from utils.regex_phone import regex_phone
from keyboards.default.product import products_keyboard
from utils.db_api.views import (
    user_detail, user_create, order_create,
    group_notify, group_notify_map)
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
    result = await user_detail(call.from_user.id)
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
    deliver_time = message.text
    if deliver_time in ("O'tqazib yuborish. ➡", "Пропуск. ➡"):
        deliver_time = 'Vaqt belgilanmagan'
    await state.update_data(data={'deliver_time': deliver_time})
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
    user_phone = result.get('result').get('phone')
    answer_text = DoneText.get(user_lang)
    await message.answer(
        text=answer_text,
        reply_markup=await products_keyboard(user_lang)
    )
    data = await state.get_data()
    products = _redis.get_user_basket(message.from_user.id)
    if data.get('product') != 'all':
        amount = products.get(data.get('product'))
        products = {data.get('product'): amount}
    products_price = _redis.get_all_products_price()
    username = ''
    if message.from_user.username:
        username = '\n@' + message.from_user.username
    notify_message = f"Foydalanuvchi: {message.from_user.full_name}{username}\n\n"
    total_price = 0
    for prod, amount in products.items():
        price = products_price.get(prod)
        await order_create(
            data={
                "user": message.from_user.id,
                "name": prod,
                "price": price,
                "total_price": int(amount) * int(price),
                "count": amount
            }
        )
        notify_message += (f"🔥 Mahsulot: {prod}\n"
                           f"🧮  {amount} x {price} = {int(amount) * int(price)} so'm\n\n")
        total_price += int(amount) * int(price)

    notify_message += (f"🔣 To'lov turi: {data.get('pay_type')}\n"
                       f"💸 Jami summa: {total_price} so'm\n\n"
                       f"🕑 Yetkazib berish vaqti: {data.get('deliver_time')}\n"
                       f"📱 Telefon raqami: {user_phone}\n"
                       f"☎ Qo'shimcha telefon raqam: {message.text}")
    location = data.get('location')
    await user_create(
        data={
            "telegram_id": message.from_user.id,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "username": message.from_user.username,
            "location": "string",
            "latitude": location.get('lat'),
            "longitude": location.get('lon'),
        }
    )
    await group_notify(
        message=notify_message
    )
    await group_notify_map(
        message=message,
        data=location
    )
    _redis.delete_user_basket(pk=message.from_user.id, _all=True)
    await state.clear()


@router.message(PaymentState.phone, lambda msg: msg.text and not regex_phone(msg.text))
async def create_phone(message: Message):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    await message.answer(
        text={
            'uz': "Iltimos ko'rsatilgan tartibda +998902223344 telefon raqam yuboring!",
            'ru': "Пожалуйста, пришлите номер телефона в указанном порядке (+998902223344)!"
        }.get(user_lang)
    )
