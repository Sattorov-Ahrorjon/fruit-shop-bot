from aiogram import Router
from . import start
from . import help
from . import echo
from . import register
from . import product
from . import basket
from . import payment

user_router = Router()
user_router.include_routers(
    help.router,
    start.router,
    register.router,
    payment.router,
    product.router,
    basket.router,
    echo.router,
)
