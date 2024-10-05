from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.src.shemas.establishment import EstablishmentSchemaOut


def get_pagination_keyboard(establishments: list[EstablishmentSchemaOut], current_page: int, total_pages: int) -> InlineKeyboardBuilder:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for establishment in establishments:
        kb_builder.row(InlineKeyboardButton(text=f'{establishment.title}', callback_data=f'establishment_{establishment.id}'), width=1)
    kb_builder.row(
        InlineKeyboardButton(
            text='<<<',
            callback_data=f'page_{current_page - 1}'
        ),
        InlineKeyboardButton(
            text=f'{current_page}/{total_pages}',
            callback_data=f'total_pages_{current_page}/{total_pages}',
        ),
        InlineKeyboardButton(
            text='>>>',
            callback_data=f'page_{current_page + 1}'
        ),
        width=3
    )
    return kb_builder.as_markup()



