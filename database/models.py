from peewee import *
from data.config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD, DB_PORT

db = PostgresqlDatabase(DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = BigIntegerField(primary_key=True)
    username = CharField(max_length=200, null=True)

    class Meta:
        db_name = 'users'


class Films(BaseModel):
    film_id = CharField(max_length=255)
    film_name = CharField(max_length=255)
    # film_genre = CharField(max_length=255)
    film_link = CharField(max_length=255)
    date = DateField(formats=['%Y-%m-%d'])

    class Meta:
        db_name = 'films'


class ChannelConfig(BaseModel):
    channel_id = CharField(max_length=150)

    class Meta:
        db_name = 'channel_config'


class SubscribeChannels(BaseModel):
    channel_id = CharField(max_length=200)
    channel_name = CharField(max_length=200)
    channel_link = CharField(max_length=200)

    class Meta:
        db_name = 'subscribe_channels'



