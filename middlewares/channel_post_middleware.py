from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update


class ChannelPostMiddleware(BaseMiddleware):
    films = []

    async def on_pre_process_update(self, update: Update, data: dict):
        self.films.append(update)
        data['films'] = self.films
