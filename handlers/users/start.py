from data.config import get_admins
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from states.register import Register
from states.target import Target
from keyboards.default.user import language
from keyboards.default.product import products_keyboard
from keyboards.inline.target import target_check
from utils.db_api.views import (
    user_create, sendAdvertisement
)

router = Router()

MainBtn = ("Главная 🏠", "Bosh sahifa 🏠")


@router.message(lambda msg: msg.text in MainBtn or msg.text == '/start')
async def bot_start(message: types.Message, state: FSMContext):
    res = await user_create(
        data={
            'telegram_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'username': message.from_user.username,
        }
    )
    if res and res.get('lang'):
        lang = res.get('lang')
        await message.answer(
            text={
                'uz': "🏠 Siz asosiy sahifadasiz\n\n"
                      "Kerakli buyuruqni tanlang 👇",
                'ru': "🏠 Вы находитесь на главной странице\n\n"
                      "Выберите нужную команду 👇"
            }.get(lang),
            reply_markup=await products_keyboard(lang)
        )
        await state.clear()
        return
    await message.answer(
        text="Assalomu alaykum. Online buyurtma berish botimizga xush kelibsiz !\n"
             "Berilgan mahsulotlardan birini tanlang 🍎\n\n"
             "Здравствуйте. Добро пожаловать в наш бот для онлайн-заказов !\n"
             "Выберите один из представленных продуктов 🍎",
        reply_markup=language()
    )
    await state.set_state(Register.lang)


@router.message(lambda msg: msg.text == '/target' and msg.from_user.id in get_admins())
async def create_advertisement(message: types.Message, state: FSMContext):
    await message.answer(
        text="Tayyorlangan reklama habaringizni telegram botga yuborishingiz mumkin\n"
             "Telegram bot barcha foydalanuchilarga bu habarni yetkazadi 🔥"
    )
    await state.set_state(Target.target)


@router.message(Target.target, lambda msg: msg.from_user.id in get_admins())
async def send_advertisement(message: types.Message, state: FSMContext):
    await state.update_data({'target': message.message_id})
    await message.reply(
        text="Ushbu habarni barchaga yuborishni tasdiqlaysizmi ?",
        reply_markup=target_check()
    )


@router.callback_query(
    Target.target, lambda call: call.data.startswith('target_send') and call.from_user.id in get_admins())
async def send_advertisement(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    success, failed = await sendAdvertisement(message=call.message, msg_id=data.get('target'))
    await call.message.answer(
        text=f"Habar muvaffaqiyatli tarqatildi\n\n"
             f"✅ {success} ta odam bordi\n"
             f"❌ {failed} ta odamga bormadi"
    )
    await state.clear()


@router.callback_query(
    Target.target, lambda call: call.data.startswith('target_cancel') and call.from_user.id in get_admins())
async def cancel_advertisement(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        text="Habar bekor qilindi ✅"
    )
    await state.clear()
