from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .channel_post_middleware import ChannelPostMiddleware


if __name__ == "middlewares":
    # dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(ChannelPostMiddleware())
