import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import *

from bot_context import *
from database.connections import add_user, get_bot_statistics, get_new_films, get_one_film, search_films
from keyboards.default.users_btn import start_menu_btn
from keyboards.inline.users_btn import new_films_btn, film_link_btn, films_btn, subscribe_btn
from loader import dp
from datetime import datetime, timedelta

from utils.misc.check_subscribe import check_user_subscribe


async def bot_start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await add_user(user_id, username)
    is_subs = await check_user_subscribe(message)
    if is_subs:
        btn = await start_menu_btn()
        await message.answer(start_text, reply_markup=btn)
    else:
        btn = await subscribe_btn()
        context = subscribe_text.format(message.from_user.first_name)
        await message.answer(context, reply_markup=btn)


async def bot_statistics_handler(message: Message):
    users, films = await get_bot_statistics()
    today = datetime.now().strftime('%Y.%m.%d %H:%M')
    context = statistics_text.format(today, users, films)
    await message.answer(context)


# async def film_ganer_handler(message: Message):
#     print(message.text, 1)


async def new_films_handler(message: Message):
    is_subs = await check_user_subscribe(message)
    if is_subs:
        films = await get_new_films()
        if films:
            btn = await new_films_btn(films)
            context = ''
            for n, item in enumerate(films, 1):
                context += f'{n}. {item["film_name"]}\n'
            await message.answer(context, reply_markup=btn)
        else:
            await message.answer("Xozircha yangi filimlar mavjud emas!")
    else:
        btn = await subscribe_btn()
        context = subscribe_text.format(message.from_user.first_name)
        await message.answer(context, reply_markup=btn)

async def find_film_handler(message: Message, state: FSMContext):
    is_subs = await check_user_subscribe(message)
    if is_subs:
        await state.finish()
        film_name = message.text
        filmss = await search_films(film_name, 1)
        if filmss:
            await state.set_data({'film_name': film_name})
            btn = await films_btn(filmss, 1, 2)
            context = f'<b>Natijalar {len(filmss)}\n\n</b>'
            for n, item in enumerate(filmss, 1):
                context += f'{n}. {item["film_name"]}\n'
            await message.answer(context, reply_markup=btn)
        else:
            await message.answer(not_found_film_text)
    else:
        btn = await subscribe_btn()
        context = subscribe_text.format(message.from_user.first_name)
        await message.answer(context, reply_markup=btn)

async def film_cancel_callback(c: CallbackQuery, state: FSMContext):
    await c.answer("Bekor qilindi!", show_alert=True)
    await c.message.delete()
    await state.finish()


async def select_film_callback(c: CallbackQuery):
    is_subs = await check_user_subscribe(c)
    if is_subs:
        await c.answer()
        film_id = c.data.split(":")[-1]
        film_link = await get_one_film(film_id)
        btn = await film_link_btn(film_link)
        await c.message.answer('<b>Yuklab olish uchun pastdagi tugmani bosing</b>', reply_markup=btn)
    else:
        btn = await subscribe_btn()
        context = subscribe_text.format(c.from_user.first_name)
        await c.message.answer(context, reply_markup=btn)

async def prev_films_callback(c: CallbackQuery, state: FSMContext):
    is_subs = await check_user_subscribe(c)
    if is_subs:
        page = c.data.split(":")[-1]
        data = await state.get_data()
        # print(int(page) - 1, 'prev')
        if int(page) - 1 > 0:
            page = int(page) - 1
            filmss = await search_films(data['film_name'], int(page))
            btn = await films_btn(filmss, int(page), int(page) + 1)
            context = f'<b>Natijalar {len(filmss)}\n\n</b>'
            for n, item in enumerate(filmss, 1):
                context += f'{n}. {item["film_name"]}\n'
            await c.message.edit_text(context, reply_markup=btn)
        else:
            await c.answer("Natija yoq!", show_alert=True)
    else:
        btn = await subscribe_btn()
        context = subscribe_text.format(c.from_user.first_name)
        await c.message.answer(context, reply_markup=btn)


async def next_films_callback(c: CallbackQuery, state: FSMContext):
    is_subs = await check_user_subscribe(c)
    if is_subs:
        page = c.data.split(":")[-1]
        data = await state.get_data()
        filmss = await search_films(data['film_name'], int(page))

        if filmss:
            # print(page, int(page)+1, 'next')
            btn = await films_btn(filmss, page, int(page)+1)
            context = f'<b>Natijalar {len(filmss)}\n\n</b>'
            for n, item in enumerate(filmss, 1):
                context += f'{n}. {item["film_name"]}\n'
            await c.message.edit_text(context, reply_markup=btn)
        else:
            await c.answer("Natija yoq!", show_alert=True)
    else:
        btn = await subscribe_btn()
        context = subscribe_text.format(c.from_user.first_name)
        await c.message.answer(context, reply_markup=btn)


async def check_user_subscribe_callback(c: CallbackQuery):
    is_subs = await check_user_subscribe(c)
    if is_subs:
        await c.message.delete()
        btn = await start_menu_btn()
        await c.message.answer(start_text, reply_markup=btn)
    else:
        btn = await subscribe_btn()
        context = subscribe_text.format(c.from_user.first_name)
        await c.message.answer(context, reply_markup=btn)


def register_users_py(dp: Dispatcher):
    dp.register_message_handler(bot_start_handler, commands=['start'])
    dp.register_message_handler(bot_statistics_handler, text='📊 Statistika')
    # dp.register_message_handler(film_ganer_handler, text='🎞 Janrlar')
    dp.register_message_handler(new_films_handler, text='🆕 Yangi kinolar')
    dp.register_message_handler(find_film_handler, content_types=['text'])

    dp.register_callback_query_handler(film_cancel_callback, text='film_cancel')
    dp.register_callback_query_handler(check_user_subscribe_callback, text='check_subscribe')
    dp.register_callback_query_handler(select_film_callback, text_contains='film:')
    dp.register_callback_query_handler(prev_films_callback, text_contains='prev:')
    dp.register_callback_query_handler(next_films_callback, text_contains='next:')
