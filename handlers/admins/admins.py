import asyncio
import sys

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import *

from bot_context import *
from database.connections import edit_channel_config, get_all_users, get_all_subscribe_channels, add_subscribe_channel, \
    delete_subscribe_channel, del_all_films
from keyboards.inline.admins_btn import admin_menu_btn, admin_channels_btn, admin_channel_btn
from loader import dp, bot
from data.config import ADMINS
from states.AllStates import Adminstate


async def admin_start_handler(message: Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        btn = await admin_menu_btn()
        await message.answer(f"Admin panel", reply_markup=btn)


async def admin_back_callback(c: CallbackQuery):
    btn = await admin_menu_btn()
    await c.message.edit_text(f"Admin panel", reply_markup=btn)


async def edit_films_channel_callback(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(edit_films_channel_text)
    await Adminstate.edit_film_channel.set()


async def edit_films_channel_state(message: Message, state: FSMContext):
    text = message.text
    if text in ['/start', '/admin']:
        btn = await admin_menu_btn()
        await message.answer(f"Admin panel", reply_markup=btn)
        return await state.finish()

    if text.isdigit():
        await edit_channel_config(text)
        await message.answer('✅')

        btn = await admin_menu_btn()
        await message.answer(f"Admin panel", reply_markup=btn)
        await state.finish()
    else:
        await message.answer("Kanal aydisini yuboring!")


async def admin_mailing_callback(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(mailing_text)
    await Adminstate.mailing.set()


async def admin_mailing_state(message: Message, state: FSMContext):
    users = await get_all_users()
    user_id = message.from_user.id
    text_type = message.content_type
    text = message.text
    text_caption = message.caption
    rep_btn = message.reply_markup
    sends = 0
    sends_error = 0

    if text in ['/start', '/admin']:
        await message.answer("Bekor qilindi")
        await state.finish()
        return

    await message.answer("Xabar yuborish boshlandi....")
    await state.finish()
    for u in users:
        try:
            if text_type == 'text':
                await bot.send_message(u['user_id'], text, reply_markup=rep_btn)
                sends += 1
                await asyncio.sleep(0.03)

            elif text_type == "photo":
                await bot.send_photo(u['user_id'], message.photo[-1].file_id, caption=text_caption,
                                     reply_markup=rep_btn)
                sends += 1
                await asyncio.sleep(0.03)

            elif text_type == "video":
                await bot.send_video(u['user_id'], message.video.file_id, caption=text_caption, reply_markup=rep_btn)
                sends += 1
                await asyncio.sleep(0.03)

            elif text_type == "animation":
                await bot.send_animation(u['user_id'], message.animation.file_id, caption=text_caption, reply_markup=rep_btn)
                sends += 1
                await asyncio.sleep(0.03)

            elif text_type == "document":
                await bot.send_document(u['user_id'], message.document.file_id, caption=text_caption, reply_markup=rep_btn)
                sends += 1
                await asyncio.sleep(0.03)


        except Exception as ex:
            print(f'{type(ex).__name__}: {ex} | Line: {sys.exc_info()[-1].tb_lineno} ****** {ex}')
            sends_error += 1
            continue

    if sends == 0:
        await bot.send_message(user_id, "⚠️ Xabar xechkimga yetibormadi")
    else:
        context = mailing_success_text.format(sends + sends_error, sends, sends_error)
        await bot.send_message(user_id, context)


async def admin_subscribe_channels_callback(c: CallbackQuery):
    await c.answer()
    channels = await get_all_subscribe_channels()
    btn = await admin_channels_btn(channels)
    await c.message.edit_text("Kanallar", reply_markup=btn)


async def admin_add_subscribe_channel_callback(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text("Kanal ID sini va linkini yuboring:\n\n"
                              "<em>Namuna: 7796789216 + Kanal nomi + https://t.me/+khjgsdfhsldkf</em>")
    await Adminstate.add_channel.set()


async def admin_add_subscribe_channel_state(message: Message, state: FSMContext):
    text = message.text
    if text in ['/start', '/admin']:
        btn = await admin_menu_btn()
        await message.answer(f"Admin panel", reply_markup=btn)
        return await state.finish()

    text = text.replace(" ", "").split("+", 2)
    if len(text) == 3:
        await add_subscribe_channel(text[0], text[2], text[1])
        await message.answer("✅ Kanal saqlandi")

        channels = await get_all_subscribe_channels()
        btn = await admin_channels_btn(channels)
        await message.answer("Kanallar", reply_markup=btn)
        return await state.finish()

    await message.answer("Format xato")


async def admin_subscribe_channel_info_callback(c: CallbackQuery):
    await c.answer()
    cd = c.data.split(":")[1]
    channel = await get_all_subscribe_channels(one=True, channel_id=cd)
    btn = await admin_channel_btn(channel['channel_link'], channel['channel_id'])
    await c.message.edit_text(f"{channel['channel_name']}", reply_markup=btn)


async def admin_delete_subscribe_channel_callback(c: CallbackQuery):
    cd = c.data.split(":")[1]
    await delete_subscribe_channel(cd)
    channels = await get_all_subscribe_channels()
    btn = await admin_channels_btn(channels)
    await c.message.edit_text("Kanallar", reply_markup=btn)
    await c.answer("✅ Kanal o'chirildi", show_alert=True)


async def delete_all_films_callback(c: CallbackQuery):
    await del_all_films()
    await c.answer("✅ Barcha kinolar o'chirildi", show_alert=True)


def register_admins_py(dp: Dispatcher):
    dp.register_message_handler(admin_start_handler, commands=['admin'])

    dp.register_callback_query_handler(edit_films_channel_callback, text='edit_films_channel')
    dp.register_callback_query_handler(admin_mailing_callback, text='mailing')
    dp.register_callback_query_handler(admin_subscribe_channels_callback, text='channels')
    dp.register_callback_query_handler(admin_back_callback, text='back')
    dp.register_callback_query_handler(admin_add_subscribe_channel_callback, text='add_channel')
    dp.register_callback_query_handler(delete_all_films_callback, text='del_all_films')
    dp.register_callback_query_handler(admin_subscribe_channel_info_callback, text_contains='channel_info:')
    dp.register_callback_query_handler(admin_delete_subscribe_channel_callback, text_contains='channel_del:')

    dp.register_message_handler(edit_films_channel_state, state=Adminstate.edit_film_channel, content_types=['text'])
    dp.register_message_handler(admin_add_subscribe_channel_state, state=Adminstate.add_channel, content_types=['text'])
    dp.register_message_handler(admin_mailing_state, state=Adminstate.mailing,
                                content_types=['text', 'document', 'video', 'photo', 'animation'])
