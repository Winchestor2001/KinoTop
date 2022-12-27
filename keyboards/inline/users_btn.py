from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.connections import get_subs_channels


async def new_films_btn(films):
    btn = InlineKeyboardMarkup(row_width=5)
    btn.add(
        *[InlineKeyboardButton(f'{n}', callback_data=f'film:{item["film_id"]}') for n, item in enumerate(films, 1)]
    )
    btn.add(
        InlineKeyboardButton('❌', callback_data='film_cancel')
    )
    return btn


async def film_link_btn(link):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton('📥 Yuklab olish', url=link)
    )
    return btn


async def films_btn(films, prev_p, next_p):
    btn = InlineKeyboardMarkup(row_width=5)
    btn.add(
        *[InlineKeyboardButton(f'{n}', callback_data=f'film:{item["film_id"]}') for n, item in enumerate(films, 1)]
    )
    btn.add(
        InlineKeyboardButton('⬅️ Ortga', callback_data=f'prev:{prev_p}'),
        InlineKeyboardButton('❌', callback_data='film_cancel'),
        InlineKeyboardButton('Oldinga ➡️', callback_data=f'next:{next_p}')
    )
    return btn


async def subscribe_btn():
    channels = await get_subs_channels()
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        *[InlineKeyboardButton(f'{item["channel_name"]}', url=f'{item["channel_link"]}') for item in channels],
        InlineKeyboardButton('✅ Tekshirish', callback_data="check_subscribe")
    )
    return btn


