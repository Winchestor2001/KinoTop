from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def admin_menu_btn():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton("Kanallar", callback_data="channels"),
        InlineKeyboardButton("Xabar yuborish", callback_data="mailing"),
        InlineKeyboardButton("Kino kanalini yangilash", callback_data="edit_films_channel"),
        InlineKeyboardButton("Barcha kinolarni o'chirish", callback_data="del_all_films"),
    )
    return btn


async def admin_channels_btn(channels):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        *[InlineKeyboardButton(f"{item['channel_name']}", callback_data=f"channel_info:{item['channel_id']}") for item in channels],
        InlineKeyboardButton("➕", callback_data="add_channel"),
        InlineKeyboardButton("Ortga", callback_data="back"),
    )
    return btn


async def admin_channel_btn(channel_link, channel_id):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("Kanalga o'tish", url=channel_link),
        InlineKeyboardButton("❌", callback_data=f"channel_del:{channel_id}"),
        InlineKeyboardButton("Ortga", callback_data="channels"),
    )
    return btn


