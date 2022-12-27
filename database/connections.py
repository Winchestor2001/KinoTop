from datetime import datetime, timedelta

from playhouse.shortcuts import model_to_dict

from data.config import ADMINS
from .models import *


async def add_user(user_id: int, username: str):
    with db:
        if not Users.select().where(Users.user_id == user_id).exists():
            Users.create(user_id=user_id, username=username)


async def get_bot_statistics():
    with db:
        users = Users.select().count()
        films = Films.select().count()
        return users, films


async def edit_channel_config(channel_id: str):
    with db:
        if ChannelConfig.select().exists():
            ChannelConfig.update(channel_id=channel_id).execute()
        else:
            ChannelConfig.create(channel_id=channel_id)


async def get_all_users():
    with db:
        users = Users.select()
        users = [model_to_dict(item) for item in users]
        return users


async def get_all_subscribe_channels(one=False, channel_id=None):
    with db:
        if one:
            channels = SubscribeChannels.select().where(SubscribeChannels.channel_id == channel_id)
            channels = [model_to_dict(item) for item in channels]
            return channels[0]

        channels = SubscribeChannels.select()
        channels = [model_to_dict(item) for item in channels]
        return channels


async def add_subscribe_channel(channel_id, channel_link, channel_name):
    with db:
        SubscribeChannels.create(channel_id=channel_id, channel_link=channel_link, channel_name=channel_name)


async def delete_subscribe_channel(channel_id):
    with db:
        SubscribeChannels.delete().where(SubscribeChannels.channel_id == channel_id).execute()


async def get_bot_channel():
    with db:
        channel = ChannelConfig.select()
        channel = [model_to_dict(item) for item in channel]
        return channel[0]


async def save_film(film_name, film_link):
    today = datetime.now().strftime('%Y-%m-%d')
    film_id = film_link.split("/")[-1]
    with db:
        Films.create(film_id=film_id, film_name=film_name, film_link=film_link, date=today)


async def get_new_films():
    _3_days_ago = datetime.now() - timedelta(days=3)
    _3_days_ago = _3_days_ago.strftime('%Y-%m-%d')
    with db:
        films = Films.select().where(Films.date >= _3_days_ago)
        films = [model_to_dict(item) for item in films]
        return films


async def get_one_film(film_id):
    with db:
        film = Films.select().where(Films.film_id == film_id)
        film = [model_to_dict(item) for item in film]
        return film[0]['film_link']


async def search_films(film_name, limit):
    with db:
        # print(limit, 'limit')
        films = Films.select().where(Films.film_name.contains(film_name)).paginate(limit, 10)
        films = [model_to_dict(item) for item in films]
        return films


async def del_all_films():
    with db:
        Films.delete().execute()


async def get_subs_channels():
    with db:
        channels = SubscribeChannels.select()
        channels = [model_to_dict(item) for item in channels]
        return channels


