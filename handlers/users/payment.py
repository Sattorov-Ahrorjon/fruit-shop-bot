from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from utils.misc.redis_service import RedisService
from utils.db_api.views import user_detail
from states.payment import PaymentState
from utils.regex_phone import regex_phone
from keyboards.default.product import products_keyboard
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
    await state.set_state(PaymentState.deliver_time)


@router.message(PaymentState.deliver_time, lambda msg: msg.text in ("O'tqazib yuborish. ➡", "Пропуск. ➡"))
async def transferred_to_location(message: Message, state: FSMContext):
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
    await state.set_state(PaymentState.phone)


@router.message(PaymentState.phone, lambda msg: msg.text and regex_phone(msg.text))
async def create_phone(message: Message, state: FSMContext):
    result = await user_detail(message.from_user.id)
    user_lang = result.get('result').get('language')
    answer_text = DoneText.get(user_lang)
    await message.answer(
        text=answer_text,
        reply_markup=await products_keyboard(user_lang)
    )
    await state.clear()
