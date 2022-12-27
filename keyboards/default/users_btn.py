from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def start_menu_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    # btn.row("🎞 Janrlar", "🆕 Yangi kinolar")
    btn.row("🆕 Yangi kinolar")
    btn.row("📊 Statistika")
    return btn
