from typing import List

from aiogram.types import Message, CallbackQuery

from database.connections import get_subs_channels
from loader import bot


async def check_user_subscribe(message):
    channels = await get_subs_channels()
    for channel in channels:
        check = await bot.get_chat_member('-100' + channel['channel_id'], message.from_user.id)
        if check.status == 'left':
            return False

    return True
