from aiogram.filters import Filter
from aiogram.types import Message
import os


ADMINS: list[int] = os.getenv('ADMINS_ID')


class AdminProtect(Filter):

    def __init__(self):
        self.admins: list[int] = ADMINS

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins