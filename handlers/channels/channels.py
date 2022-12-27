from typing import List

from aiogram import Dispatcher
from aiogram.types import *

from bot_context import subscribe_channel_link_text
from database.connections import get_bot_channel, save_film
from loader import dp
from utils.misc.film_context_formatter import context_formatter


async def get_channel_post_handler(message: Message):
    channel_id = await get_bot_channel()
    if channel_id['channel_id'] == str(message.chat.id)[4:]:
        film_link = subscribe_channel_link_text.format(message.chat.username, str(message.message_id))
        caption = message.caption
        await context_formatter(caption)
        film_gener, film_name = await context_formatter(caption)
        if film_gener:
            await save_film(film_name, film_link)
        else:
            await save_film(film_name, film_link)


def register_channels_py(dp: Dispatcher):
    dp.register_channel_post_handler(get_channel_post_handler, content_types=['video'])
