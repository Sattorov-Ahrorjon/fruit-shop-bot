from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from utils.db_api.views import user_create
from states.register import Register
from keyboards.default.user import language
from keyboards.default.product import products_keyboard

router = Router()

MainBtn = ["Главная 🏠", "Bosh sahifa 🏠"]


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
    lang = res.get('lang')
    reply_btn = language()
    msg_text = ("Assalomu alaykum. Online buyurtma berish botimizga xush kelibsiz !\n"
                "Berilgan mahsulotlardan birini tanlang 🍎\n\n"
                "Здравствуйте. Добро пожаловать в наш бот для онлайн-заказов !\n"
                "Выберите один из представленных продуктов 🍎")
    await state.set_state(Register.lang)
    if lang:
        msg_text = {
            'uz': "Assalomu alaykum. Online buyurtma berish botimizga xush kelibsiz !\n"
                  "Berilgan mahsulotlardan birini tanlang 🍎\n\n",
            'ru': "Здравствуйте. Добро пожаловать в наш бот для онлайн-заказов !\n"
                  "Выберите один из представленных продуктов 🍎"
        }.get(lang)
        reply_btn = await products_keyboard(lang)
        await state.clear()
    await message.answer(
        text=msg_text,
        reply_markup=reply_btn
    )
