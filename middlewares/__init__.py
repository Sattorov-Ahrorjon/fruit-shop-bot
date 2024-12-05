from loader import dp
from .checkType import CheckChatTypeMiddleware

if __name__ == "middlewares":
    dp.message.middleware(CheckChatTypeMiddleware())
