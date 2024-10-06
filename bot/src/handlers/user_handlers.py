from typing import Any
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from geopy.geocoders import Yandex
import os
from bot.src.models.establishment import Establishment
from bot.src.repository.user_repository import UserRepository
from bot.src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from bot.src.schemas.establishment import EstablishmentSchemaOut
from bot.src.states.location import LocationState
from bot.src.keyboards.inline_keyboards import get_pagination_keyboard, get_route, get_location_from_user
from bot.src.repository.establishments_repository import EstablishmentRepository



user_router: Router = Router()
api_key: str = os.getenv('API_KEY')
geolocator: Yandex = Yandex(api_key=api_key)
token = os.getenv('TOKEN_BOT')




@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, session: AsyncSession):
    user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)
    if not user:
        await UserRepository.add(session=session, user_id=message.from_user.id)
    await message.answer('Введите команду /restaurants\nЧтобы посмотреть все рестораны')



@user_router.message(StateFilter(default_state), Command('restaurants'))
async def get_restaurants(message: Message, session: AsyncSession):
    current_page: int = 1
    offset: int = (current_page - 1) * 10

    res, total_count = await EstablishmentRepository.find_all_limit_offset(session=session, limit=10, offset=offset)
    establishments: list[EstablishmentSchemaOut] = [EstablishmentSchemaOut.model_validate(est) for est in res]

    total_pages: int = (total_count - 1) // 10 + 1
    

    await message.answer(
        f'Рестораны:\n',
        reply_markup=get_pagination_keyboard(establishments=establishments, current_page=current_page, total_pages=total_pages)
    )



@user_router.callback_query(StateFilter(default_state), F.data.startswith('page_'))
async def handle_pagination(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    page: int = int(callback.data.split("_")[1])
    offset: int = (page - 1) * 10
    res, total_count = await EstablishmentRepository.find_all_limit_offset(session=session, limit=10, offset=offset)
    establishments: list[EstablishmentSchemaOut] = [EstablishmentSchemaOut.model_validate(est) for est in res]

    total_pages: int = (total_count - 1) // 10 + 1
    if page > 0 and page <= total_pages:
        await callback.message.edit_text(
            'Все рестораны: \n',
            reply_markup=get_pagination_keyboard(establishments, page, total_pages)
        )
        


@user_router.callback_query(StateFilter(default_state), F.data.startswith('total_pages'))
async def total_pages(callback: CallbackQuery):
    res: str = callback.data.split('_')[2]
    await callback.answer(f'Страницы: {res}')


@user_router.callback_query(StateFilter(default_state), F.data.startswith('establishment_'))
async def get_establishment(callback: CallbackQuery, session: AsyncSession):
    res: str = callback.data.split('_')[1]
    establisment: Establishment = await EstablishmentRepository.find_one_or_none(session=session, id=int(res))
    establisment_out: EstablishmentSchemaOut = EstablishmentSchemaOut.model_validate(establisment)
    await callback.message.edit_text(text='Информация о ресторане:')
    await callback.message.answer_photo(
        photo=establisment.photo_url,
        caption=
        f'<b>ID: {establisment_out.id}</b>'
        f'<b>{establisment_out.title}</b>\n\n'
        f'<b>{establisment_out.description}</b>\n\n'
        f'<b>{establisment_out.address}</b>',
        reply_markup=get_location_from_user(rest_id=establisment.id)
    )





    
    

@user_router.callback_query(StateFilter(default_state), F.data.startswith('route_'))
async def cmd_location(callback: CallbackQuery, state: FSMContext):
    rest_id: str = callback.data.split('_')[1]
    await callback.answer()
    await callback.message.answer('Отправьте свою геопозицю, чтобы построить маршрут до ресторана')
    await state.set_state(LocationState.location)
    await state.update_data({'rest_id': rest_id})
    


@user_router.message(StateFilter(LocationState.location), F.location)
async def get_location(message: Message, session: AsyncSession, state: FSMContext):
    data: dict = await state.get_data()
    rest_id: int = data['rest_id']
    establishment: Establishment = await EstablishmentRepository.find_one_or_none(session=session, id=rest_id)
    address_from_user: str = geolocator.reverse((message.location.latitude, message.location.longitude))
    await message.answer('Маршрут построен', reply_markup=get_route(
        latitude=message.location.latitude,
        longitude=message.location.longitude,
        address_from_user=address_from_user,
        address=establishment.address
    ))
    await state.clear()
    

@user_router.message(StateFilter(LocationState.location), ~F.location)
async def get_location_warning(message: Message):
    await message.answer('Вы должны отправить вашу геопозицию.')

