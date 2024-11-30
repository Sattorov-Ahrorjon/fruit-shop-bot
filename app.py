import asyncio
import middlewares
from loader import dp, bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers.users.routes import user_router


async def on_startup():
    # Birlamchi komandalar (/star va /help)
    await set_default_commands()

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(bot)

    # Include user routers
    dp.include_router(user_router)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(on_startup())
    # executor.start_polling(dp, on_startup=on_startup)
