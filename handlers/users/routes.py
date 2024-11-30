from aiogram import Router
from . import start
from . import help
from . import echo
from . import register

user_router = Router()
user_router.include_routers(
    help.router,
    start.router,
    register.router,
    echo.router,
)
