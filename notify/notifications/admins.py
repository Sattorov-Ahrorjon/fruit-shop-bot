from data.config import NOTIFY_CHANNEL_ID


async def new_user_addition_notification(about_user, bot):
    await bot.send_message(text="Bot ishga tushdi.", chat_id=NOTIFY_CHANNEL_ID)
    await bot.send_message(text=about_user, chat_id=NOTIFY_CHANNEL_ID)
