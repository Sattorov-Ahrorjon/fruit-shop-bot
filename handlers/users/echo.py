from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from .start import bot_start

router = Router()

MainBtn = ("Главная 🏠", "Bosh sahifa 🏠")


@router.message()
async def eco(message: types.Message, state: FSMContext):
    await bot_start(message, state)
