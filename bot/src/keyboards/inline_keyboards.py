from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.src.schemas.establishment import EstablishmentSchemaOut


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


def get_location_from_user(rest_id: int) -> InlineKeyboardMarkup:
    inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Построить маршрут', callback_data=f'route_{rest_id}')
            ]
        ]
    )
    return inline_kb


def get_route(latitude: float, longitude: float, address_from_user: str, address: str) -> InlineKeyboardMarkup:
    inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Маршрут построен', 
                    web_app=WebAppInfo(url=f'https://17fe-78-85-48-141.ngrok-free.app/?latitude={latitude}&longitude={longitude}&start_address={address_from_user}&end_address={address}'))
            ]
        ]
    )
    return inline_kb
