from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import os


URL: str = os.getenv('WEBHOOK_URL')



def add_establishment(token: str) -> InlineKeyboardMarkup:
    inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить новое заведение', web_app=WebAppInfo(url=f'{URL}/add_establishment/?token={token}'))
            ]
        ]
    )
    return inline_kb
