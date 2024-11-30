from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.regex_phone import regex_phone
from states.register import Register
from keyboards.default.user import language, phone_number_btn
from keyboards.default.product import products_keyboard
from utils.db_api.views import user_create

router = Router()

Text = {
    'askForPhone': {
        'uz': "Iltimos telefon raqamingizni\n"
              "Telefon raqam 📱 tugmasi orqali yoki\n"
              "+998901234455 ko'rinishda yuboring.",
        'ru': "Ваш номер телефона, пожалуйста\n"
              "Номер телефона через кнопку 📱 или\n"
              "«Отправить на номер +998901234455»."
    },
    'successfullyRegistered': {
        'uz': "Ro'yxatdan o'tish muvaffaqiyatli amalga oshirildi 🔥\n"
              "Berilgan mahsulotlardan birini tanlang 🍇🍎",
        'ru': "Регистрация прошла успешно 🔥\n"
              " «Выберите один из предложенных товаров 🍇🍎»",
    }
}


def regex_lang(text: str):
    return text in ("O'zbek tili 🇺🇿", "Русский язык 🇷🇺")


@router.message(Register.lang, lambda msg: msg.text and not regex_lang(msg.text))
async def save_language(message: Message, state: FSMContext):
    await message.answer(
        text="Iltimos berilgan tillardan birini tanlang!\n"
             "Пожалуйста, выберите один из указанных языков!",
        reply_markup=language()
    )
    await state.set_state(Register.lang)


@router.message(Register.lang, lambda msg: msg.text and regex_lang(msg.text))
async def save_language(message: Message, state: FSMContext):
    lang = {
        "O'zbek tili 🇺🇿": 'uz',
        "Русский язык 🇷🇺": 'ru'
    }.get(message.text)
    msg_text = Text.get('askForPhone').get(lang)
    await message.answer(
        text=msg_text,
        reply_markup=phone_number_btn()
    )
    await state.update_data(data={'lang': lang})
    await state.set_state(Register.phone)


@router.message(Register.phone, lambda msg: msg.text and not regex_phone(msg.text))
async def phone_number(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')
    msg_text = Text.get('askForPhone').get(lang)
    await message.answer(
        text=msg_text,
        reply_markup=phone_number_btn()
    )
    await state.set_state(Register.phone)


@router.message(Register.phone, lambda msg: msg.text and regex_phone(msg.text))
async def phone_number(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')
    msg_text = Text.get('successfullyRegistered').get(lang)
    await message.answer(
        text=msg_text,
        reply_markup=await products_keyboard()
    )
    await user_create(
        data={
            'telegram_id': message.from_user.id,
            'phone': message.text,
            'language': lang
        }
    )
    await state.clear()


@router.message(Register.phone, lambda msg: msg.contact is None)
async def phone_number(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')
    msg_text = Text.get('askForPhone').get(lang)
    await message.answer(
        text=msg_text,
        reply_markup=phone_number_btn()
    )
    await state.set_state(Register.phone)


@router.message(Register.phone, lambda msg: msg.contact is not None)
async def phone_number(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    data = await state.get_data()
    lang = data.get('lang')
    msg_text = Text.get('successfullyRegistered').get(lang)
    await message.answer(
        text=msg_text,
        reply_markup=await products_keyboard()
    )
    await user_create(
        data={
            'telegram_id': message.from_user.id,
            'phone': phone,
            'language': lang
        }
    )
    await state.clear()
