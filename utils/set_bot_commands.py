from aiogram.types import BotCommand, BotCommandScopeDefault
from loader import bot


async def set_default_commands():
    commands = [
        BotCommand(
            command="start",
            description="Botni ishga tushirish."
        ),
        BotCommand(
            command="help",
            description="Yordam."
        )
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
